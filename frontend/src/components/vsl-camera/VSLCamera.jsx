/**
 * VSL Camera Component
 * Camera component for realtime VSL recognition
 *
 * USAGE:
 *   <VSLCamera onDetection={handleDetection} />
 */
import { useState, useRef, useEffect } from 'react';
import { Box, Button, Card, Typography, Alert } from '@mui/material';
import { Videocam, Stop } from '@mui/icons-material';
import Webcam from 'react-webcam';

export default function VSLCamera({ onDetection, onError }) {
  const [isActive, setIsActive] = useState(false);
  const [detection, setDetection] = useState(null);
  const [error, setError] = useState(null);
  const webcamRef = useRef(null);
  const intervalRef = useRef(null);

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user"
  };

  const startCamera = () => {
    setIsActive(true);
    setError(null);

    // Start detection loop (every 500ms)
    // STUDENT TODO: Implement actual detection
    intervalRef.current = setInterval(() => {
      if (webcamRef.current) {
        const imageSrc = webcamRef.current.getScreenshot();
        if (imageSrc) {
          // PLACEHOLDER: Call detection API
          console.log('Captured frame for detection');
          // onDetection?.({ gesture: 'PLACEHOLDER', confidence: 0.0 });
        }
      }
    }, 500);
  };

  const stopCamera = () => {
    setIsActive(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };

  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  const handleUserMediaError = (err) => {
    console.error('Camera error:', err);
    setError('Không thể truy cập camera. Vui lòng kiểm tra quyền truy cập.');
    onError?.(err);
  };

  return (
    <Card sx={{ p: 2 }}>
      <Box sx={{ textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          Camera VSL Recognition
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box sx={{
          position: 'relative',
          width: '100%',
          maxWidth: 640,
          margin: '0 auto',
          mb: 2,
          borderRadius: 2,
          overflow: 'hidden',
          bgcolor: 'black'
        }}>
          {isActive ? (
            <Webcam
              ref={webcamRef}
              audio={false}
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              onUserMediaError={handleUserMediaError}
              style={{ width: '100%', display: 'block' }}
            />
          ) : (
            <Box sx={{
              height: 360,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white'
            }}>
              <Typography>Camera chưa bật</Typography>
            </Box>
          )}

          {detection && (
            <Box sx={{
              position: 'absolute',
              bottom: 10,
              left: 10,
              right: 10,
              bgcolor: 'rgba(0,0,0,0.7)',
              color: 'white',
              p: 1,
              borderRadius: 1
            }}>
              <Typography variant="body2">
                Detected: {detection.gesture} ({(detection.confidence * 100).toFixed(1)}%)
              </Typography>
            </Box>
          )}
        </Box>

        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
          {!isActive ? (
            <Button
              variant="contained"
              color="primary"
              startIcon={<Videocam />}
              onClick={startCamera}
            >
              Bắt đầu
            </Button>
          ) : (
            <Button
              variant="contained"
              color="error"
              startIcon={<Stop />}
              onClick={stopCamera}
            >
              Dừng
            </Button>
          )}
        </Box>
      </Box>
    </Card>
  );
}
