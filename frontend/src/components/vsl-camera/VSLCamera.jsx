/**
 * VSL Camera Component
 * Camera component for realtime VSL recognition with hand keypoint tracking
 *
 * FEATURES:
 * - Camera device selection
 * - Real-time hand keypoint detection
 * - Visual keypoint overlay on video
 * - Live keypoint data display
 *
 * WORKFLOW:
 * 1. Select Camera -> 2. Start Camera -> 3. Start Detection -> 4. View Keypoints on Video
 *
 * USAGE:
 *   <VSLCamera onDetection={handleDetection} />
 */
import { useState, useRef, useEffect } from 'react';
import {
  Box, Button, Card, Typography, Alert, Paper,
  FormControl, InputLabel, Select, MenuItem, IconButton, Divider
} from '@mui/material';
import { Videocam, Stop, Refresh, PlayArrow, Visibility } from '@mui/icons-material';
import Webcam from 'react-webcam';

export default function VSLCamera({ onDetection, onError }) {
  // Camera states
  const [devices, setDevices] = useState([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState('');
  const [cameraStarted, setCameraStarted] = useState(false);

  // Detection states
  const [isDetecting, setIsDetecting] = useState(false);
  const [error, setError] = useState(null);
  const [keypointsData, setKeypointsData] = useState('');
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [handsDetected, setHandsDetected] = useState(0);
  const [currentKeypoints, setCurrentKeypoints] = useState(null);

  const webcamRef = useRef(null);
  const canvasRef = useRef(null);
  const intervalRef = useRef(null);
  const websocketRef = useRef(null);

  // WebSocket URL
  const WS_URL = 'ws://localhost:8000/api/v1/vsl/hand-tracking/realtime';

  // Enumerate camera devices
  const handleDevices = (mediaDevices) => {
    const videoDevices = mediaDevices.filter(({ kind }) => kind === 'videoinput');
    setDevices(videoDevices);
    if (videoDevices.length > 0 && !selectedDeviceId) {
      setSelectedDeviceId(videoDevices[0].deviceId);
    }
  };

  // Load available cameras on mount
  useEffect(() => {
    navigator.mediaDevices.enumerateDevices().then(handleDevices);
  }, []);

  // Refresh camera list
  const refreshCameras = async () => {
    try {
      const mediaDevices = await navigator.mediaDevices.enumerateDevices();
      handleDevices(mediaDevices);
    } catch (err) {
      console.error('Error enumerating devices:', err);
      setError('Failed to refresh camera list');
    }
  };

  // Start camera display
  const startCamera = () => {
    if (!selectedDeviceId) {
      setError('Please select a camera first');
      return;
    }
    setCameraStarted(true);
    setError(null);
  };

  // Stop camera display
  const stopCamera = () => {
    setCameraStarted(false);
    stopDetection();
  };

  // Start detection
  const startDetection = () => {
    if (!cameraStarted) {
      setError('Please start camera first');
      return;
    }

    setIsDetecting(true);
    setError(null);
    setKeypointsData('Connecting to hand tracking server...\n');

    try {
      // Create WebSocket connection
      const ws = new WebSocket(WS_URL);
      websocketRef.current = ws;

      ws.onopen = () => {
        console.log('[WebSocket] Connected to hand tracking server');
        setConnectionStatus('connected');
        setKeypointsData('Connected! Detecting hands...\n');

        // Start sending frames to backend (every 200ms for ~5 FPS)
        intervalRef.current = setInterval(() => {
          if (webcamRef.current && ws.readyState === WebSocket.OPEN) {
            const imageSrc = webcamRef.current.getScreenshot();
            if (imageSrc) {
              // Send base64 frame to backend
              ws.send(imageSrc);
            }
          }
        }, 200);
      };

      ws.onmessage = (event) => {
        try {
          const result = JSON.parse(event.data);

          if (result.success) {
            setHandsDetected(result.hands_detected);
            setCurrentKeypoints(result);

            // Draw keypoints on canvas
            drawKeypoints(result);

            // Format keypoints for display
            let displayText = `=== Frame Update ===\n`;
            displayText += `Hands Detected: ${result.hands_detected}\n`;
            displayText += `Processing Time: ${(result.processing_time * 1000).toFixed(1)}ms\n\n`;

            if (result.hands_detected > 0) {
              result.hands.forEach((hand) => {
                displayText += `--- ${hand.hand_type} Hand ---\n`;
                displayText += `Keypoints: ${hand.keypoints.length}\n`;

                // Show first 5 keypoints as sample
                hand.keypoints.slice(0, 5).forEach((kp) => {
                  displayText += `  Point ${kp.id}: x=${kp.x.toFixed(3)}, y=${kp.y.toFixed(3)}, z=${kp.z.toFixed(3)}\n`;
                });

                if (hand.keypoints.length > 5) {
                  displayText += `  ... and ${hand.keypoints.length - 5} more keypoints\n`;
                }
                displayText += '\n';
              });
            } else {
              displayText += 'No hands detected.\n';
              displayText += 'Show your hands to the camera.\n\n';
            }

            setKeypointsData(displayText);

            // Call parent callback if provided
            onDetection?.(result);
          } else {
            setKeypointsData(`Error: ${result.error}\n`);
          }
        } catch (err) {
          console.error('[WebSocket] Error parsing message:', err);
        }
      };

      ws.onerror = (err) => {
        console.error('[WebSocket] Error:', err);
        setConnectionStatus('error');
        setError('WebSocket error. Make sure backend is running.');
        onError?.(new Error('WebSocket connection failed'));
      };

      ws.onclose = () => {
        console.log('[WebSocket] Connection closed');
        setConnectionStatus('disconnected');
        if (isDetecting) {
          setKeypointsData(prev => prev + '\nConnection closed.\n');
        }
      };

    } catch (err) {
      console.error('[WebSocket] Failed to create connection:', err);
      setError('Failed to connect to hand tracking server');
      setIsDetecting(false);
    }
  };

  // Stop detection
  const stopDetection = () => {
    setIsDetecting(false);
    setConnectionStatus('disconnected');
    setHandsDetected(0);
    setCurrentKeypoints(null);

    // Stop frame capture interval
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    // Close WebSocket connection
    if (websocketRef.current) {
      if (websocketRef.current.readyState === WebSocket.OPEN) {
        websocketRef.current.close();
      }
      websocketRef.current = null;
    }

    // Clear canvas
    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext('2d');
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    }

    setKeypointsData('Detection stopped.\n');
  };

  // Draw keypoints on canvas
  const drawKeypoints = (result) => {
    if (!canvasRef.current || !webcamRef.current) return;

    const canvas = canvasRef.current;
    const video = webcamRef.current.video;
    const ctx = canvas.getContext('2d');

    // Match canvas size to video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Clear previous drawings
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (result.hands_detected === 0) return;

    // Hand landmark connections (MediaPipe Hands)
    const connections = [
      // Thumb
      [0, 1], [1, 2], [2, 3], [3, 4],
      // Index
      [0, 5], [5, 6], [6, 7], [7, 8],
      // Middle
      [0, 9], [9, 10], [10, 11], [11, 12],
      // Ring
      [0, 13], [13, 14], [14, 15], [15, 16],
      // Pinky
      [0, 17], [17, 18], [18, 19], [19, 20],
      // Palm
      [5, 9], [9, 13], [13, 17]
    ];

    result.hands.forEach((hand) => {
      const color = hand.hand_type === 'Left' ? '#00ff00' : '#ff0000';

      // Draw connections
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      connections.forEach(([start, end]) => {
        const startPoint = hand.keypoints[start];
        const endPoint = hand.keypoints[end];

        ctx.beginPath();
        ctx.moveTo(startPoint.x * canvas.width, startPoint.y * canvas.height);
        ctx.lineTo(endPoint.x * canvas.width, endPoint.y * canvas.height);
        ctx.stroke();
      });

      // Draw keypoints
      ctx.fillStyle = color;
      hand.keypoints.forEach((kp, idx) => {
        const x = kp.x * canvas.width;
        const y = kp.y * canvas.height;

        ctx.beginPath();
        ctx.arc(x, y, idx === 0 ? 8 : 5, 0, 2 * Math.PI);
        ctx.fill();

        // Draw wrist label
        if (idx === 0) {
          ctx.fillStyle = 'white';
          ctx.font = '12px Arial';
          ctx.fillText(hand.hand_type, x + 10, y - 10);
          ctx.fillStyle = color;
        }
      });
    });
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      if (websocketRef.current) {
        websocketRef.current.close();
      }
    };
  }, []);

  const handleUserMediaError = (err) => {
    console.error('Camera error:', err);
    setError('Cannot access camera. Please check permissions.');
    onError?.(err);
  };

  return (
    <Card sx={{ p: 2 }}>
      <Box>
        <Typography variant="h6" gutterBottom align="center">
          Real-time Hand Keypoint Detection
        </Typography>

        {/* Step 1: Camera Selection */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Step 1: Select Camera
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <FormControl fullWidth>
              <InputLabel>Camera Device</InputLabel>
              <Select
                value={selectedDeviceId}
                onChange={(e) => setSelectedDeviceId(e.target.value)}
                label="Camera Device"
                disabled={cameraStarted}
              >
                {devices.map((device) => (
                  <MenuItem key={device.deviceId} value={device.deviceId}>
                    {device.label || `Camera ${devices.indexOf(device) + 1}`}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <IconButton
              color="primary"
              onClick={refreshCameras}
              disabled={cameraStarted}
              title="Refresh camera list"
            >
              <Refresh />
            </IconButton>
          </Box>
        </Box>

        <Divider sx={{ mb: 2 }} />

        {/* Connection Status */}
        <Box sx={{ mb: 2, display: 'flex', gap: 1, justifyContent: 'center', alignItems: 'center' }}>
          <Box
            sx={{
              width: 10,
              height: 10,
              borderRadius: '50%',
              bgcolor: connectionStatus === 'connected' ? 'success.main' :
                       connectionStatus === 'error' ? 'error.main' : 'grey.400'
            }}
          />
          <Typography variant="caption" color="text.secondary">
            {connectionStatus === 'connected' ? 'Detection Active' :
             connectionStatus === 'error' ? 'Connection Error' : 'Not Detecting'}
          </Typography>
          {handsDetected > 0 && (
            <Typography variant="caption" color="primary" sx={{ ml: 2 }}>
              {handsDetected} hand{handsDetected > 1 ? 's' : ''} detected
            </Typography>
          )}
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        {/* Step 2: Camera Feed with Canvas Overlay */}
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Step 2: Camera View
          </Typography>
          <Box sx={{
            position: 'relative',
            width: '100%',
            maxWidth: 640,
            margin: '0 auto',
            borderRadius: 2,
            overflow: 'hidden',
            bgcolor: 'black'
          }}>
            {cameraStarted ? (
              <>
                <Webcam
                  ref={webcamRef}
                  audio={false}
                  screenshotFormat="image/jpeg"
                  videoConstraints={{
                    deviceId: selectedDeviceId,
                    width: 1280,
                    height: 720
                  }}
                  onUserMediaError={handleUserMediaError}
                  style={{ width: '100%', display: 'block' }}
                />
                {/* Canvas overlay for drawing keypoints */}
                <canvas
                  ref={canvasRef}
                  style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    pointerEvents: 'none'
                  }}
                />
              </>
            ) : (
              <Box sx={{
                height: 360,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                flexDirection: 'column',
                gap: 1
              }}>
                <Videocam sx={{ fontSize: 48, opacity: 0.5 }} />
                <Typography>Select a camera and click "Start Camera"</Typography>
              </Box>
            )}
          </Box>
        </Box>

        {/* Step 3: Control Buttons */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Step 3: Detection Controls
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
            {!cameraStarted ? (
              <Button
                variant="contained"
                color="primary"
                startIcon={<Videocam />}
                onClick={startCamera}
                disabled={!selectedDeviceId}
              >
                Start Camera
              </Button>
            ) : (
              <>
                <Button
                  variant="contained"
                  color="error"
                  startIcon={<Stop />}
                  onClick={stopCamera}
                >
                  Stop Camera
                </Button>
                {!isDetecting ? (
                  <Button
                    variant="contained"
                    color="success"
                    startIcon={<PlayArrow />}
                    onClick={startDetection}
                  >
                    Start Detection
                  </Button>
                ) : (
                  <Button
                    variant="contained"
                    color="warning"
                    startIcon={<Stop />}
                    onClick={stopDetection}
                  >
                    Stop Detection
                  </Button>
                )}
              </>
            )}
          </Box>
        </Box>

        <Divider sx={{ mb: 2 }} />

        {/* Step 4: Keypoints Display Area */}
        <Box>
          <Typography variant="subtitle2" gutterBottom>
            Step 4: Keypoint Data (Real-time)
          </Typography>
          <Paper
            elevation={2}
            sx={{
              p: 2,
              bgcolor: 'grey.50',
              maxHeight: 300,
              overflow: 'auto'
            }}
          >
            <Box
              component="pre"
              sx={{
                fontFamily: 'monospace',
                fontSize: '0.75rem',
                whiteSpace: 'pre-wrap',
                wordWrap: 'break-word',
                m: 0,
                p: 1,
                bgcolor: 'white',
                borderRadius: 1,
                border: '1px solid',
                borderColor: 'grey.300',
                minHeight: 100
              }}
            >
              {keypointsData || 'No data yet. Start detection to see keypoints.'}
            </Box>
          </Paper>
        </Box>

        {/* Instructions */}
        <Alert severity="info" sx={{ mt: 2 }}>
          <Typography variant="body2">
            <strong>Instructions:</strong>
            <br />
            1. Select camera and click "Refresh" if needed
            <br />
            2. Click "Start Camera" to view video feed
            <br />
            3. Click "Start Detection" to begin hand tracking
            <br />
            4. Keypoints will appear as colored dots on your hands (Green=Left, Red=Right)
          </Typography>
        </Alert>
      </Box>
    </Card>
  );
}
