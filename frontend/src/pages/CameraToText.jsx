import { useState, useRef } from 'react'
import {
  Box,
  Typography,
  Button,
  Paper,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Divider,
  Chip,
} from '@mui/material'
import {
  Videocam as VideocamIcon,
  CloudUpload as CloudUploadIcon,
  Stop as StopIcon,
} from '@mui/icons-material'
import VSLCamera from '../components/vsl-camera/VSLCamera'
import { vslRecognitionAPI } from '../services/api'

export default function CameraToText() {
  const [mode, setMode] = useState('upload') // 'upload' or 'camera'
  const [isRecording, setIsRecording] = useState(false)
  const [videoFile, setVideoFile] = useState(null)
  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [keypointsData, setKeypointsData] = useState('')

  const webcamRef = useRef(null)
  const fileInputRef = useRef(null)

  const handleFileUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
      setVideoFile(file)
      setResult(null)
      setError(null)
    }
  }

  const handleProcessVideo = async () => {
    if (!videoFile) {
      setError('Vui lòng chọn video file')
      return
    }

    setProcessing(true)
    setError(null)
    setKeypointsData('Processing video...\n')

    try {
      console.log('[CameraToText] Processing video for hand keypoints:', videoFile.name)
      const response = await vslRecognitionAPI.handTrackingVideo(videoFile, {
        sample_rate: 5,
        max_frames: null // Process all frames
      })

      setResult(response.data)
      console.log('[CameraToText] Result:', response.data)

      // Format keypoints data for display
      if (response.data.success) {
        let displayText = `=== Video Processing Complete ===\n\n`
        displayText += `Total Frames Processed: ${response.data.total_frames_processed}\n`
        displayText += `Hands Detected in: ${response.data.hands_detected_frames} frames (${response.data.detection_rate}%)\n`
        displayText += `Processing Time: ${response.data.processing_time}s\n\n`

        displayText += `=== Summary ===\n`
        displayText += `Left Hand Frames: ${response.data.summary.left_hand_frames}\n`
        displayText += `Right Hand Frames: ${response.data.summary.right_hand_frames}\n`
        displayText += `Both Hands Frames: ${response.data.summary.both_hands_frames}\n`
        displayText += `Average Hands per Frame: ${response.data.summary.avg_hands_per_frame}\n`
        displayText += `Video FPS: ${response.data.summary.video_fps}\n`
        displayText += `Video Duration: ${response.data.summary.video_duration_seconds}s\n\n`

        displayText += `=== Sample Frames (showing ${response.data.sample_frames.length}) ===\n\n`

        response.data.sample_frames.forEach((frame, idx) => {
          displayText += `Frame #${frame.frame_number} (${frame.timestamp}s):\n`
          displayText += `  Hands: ${frame.hands_detected}\n`

          if (frame.hands_detected > 0) {
            frame.hands.forEach(hand => {
              displayText += `  - ${hand.hand_type} Hand (${hand.total_keypoints} keypoints)\n`
              displayText += `    Sample keypoints:\n`
              hand.keypoints.forEach(kp => {
                displayText += `      Point ${kp.id}: x=${kp.x.toFixed(3)}, y=${kp.y.toFixed(3)}, z=${kp.z.toFixed(3)}\n`
              })
            })
          }
          displayText += '\n'
        })

        setKeypointsData(displayText)
      }
    } catch (err) {
      console.error('[CameraToText] Error:', err)
      setError('Lỗi khi xử lý video: ' + (err.response?.data?.error || err.message))
      setKeypointsData(`Error: ${err.message}\n`)
    } finally {
      setProcessing(false)
    }
  }

  const handleCameraCapture = () => {
    // TODO: Implement camera capture and processing
    console.log('[CameraToText] Camera capture clicked')
    alert('Chức năng camera đang được phát triển')
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Camera / Video → Text
      </Typography>
      <Typography variant="body1" paragraph color="text.secondary">
        Nhận diện ngôn ngữ ký hiệu VSL từ camera hoặc video và chuyển thành text
      </Typography>

      {/* Mode Selection */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
          <Button
            variant={mode === 'upload' ? 'contained' : 'outlined'}
            onClick={() => setMode('upload')}
            startIcon={<CloudUploadIcon />}
          >
            Upload Video
          </Button>
          <Button
            variant={mode === 'camera' ? 'contained' : 'outlined'}
            onClick={() => setMode('camera')}
            startIcon={<VideocamIcon />}
          >
            Camera Realtime
          </Button>
        </Box>
      </Paper>

      {/* Upload Mode */}
      {mode === 'upload' && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Upload Video File
          </Typography>

          <Box sx={{ mb: 2 }}>
            <input
              ref={fileInputRef}
              type="file"
              accept="video/*"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
            <Button
              variant="contained"
              onClick={() => fileInputRef.current?.click()}
              startIcon={<CloudUploadIcon />}
            >
              Chọn Video
            </Button>
          </Box>

          {videoFile && (
            <Alert severity="info" sx={{ mb: 2 }}>
              Đã chọn: {videoFile.name} ({(videoFile.size / 1024 / 1024).toFixed(2)} MB)
            </Alert>
          )}

          <Button
            variant="contained"
            color="primary"
            onClick={handleProcessVideo}
            disabled={!videoFile || processing}
            fullWidth
            sx={{ mt: 2 }}
          >
            {processing ? (
              <>
                <CircularProgress size={24} sx={{ mr: 1 }} />
                Đang xử lý...
              </>
            ) : (
              'Nhận diện VSL'
            )}
          </Button>
        </Paper>
      )}

      {/* Camera Mode */}
      {mode === 'camera' && (
        <Box sx={{ mb: 3 }}>
          <VSLCamera
            onDetection={(detection) => {
              console.log('Detection:', detection);
              setResult(detection);
            }}
            onError={(err) => {
              setError('Lỗi camera: ' + err.message);
            }}
          />
          <Alert severity="info" sx={{ mt: 2 }}>
            Chức năng realtime camera đang được phát triển bởi sinh viên
          </Alert>
        </Box>
      )}

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Result Display */}
      {result && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Hand Keypoint Detection Results
            </Typography>
            <Divider sx={{ mb: 2 }} />

            <Box sx={{ mb: 2 }}>
              <Chip
                label={result.success ? 'Success' : 'Failed'}
                color={result.success ? 'success' : 'error'}
                sx={{ mb: 1 }}
              />
            </Box>

            {result.total_frames_processed !== undefined && (
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Frames Processed: {result.total_frames_processed}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Hands Detected: {result.hands_detected_frames} frames ({result.detection_rate}%)
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Processing Time: {result.processing_time}s
                </Typography>
              </Box>
            )}

            {/* Keypoints Display */}
            <Paper
              elevation={2}
              sx={{
                p: 2,
                bgcolor: 'grey.50',
                maxHeight: 400,
                overflow: 'auto'
              }}
            >
              <Typography variant="subtitle2" gutterBottom>
                Hand Keypoints Data:
              </Typography>
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
                  minHeight: 150
                }}
              >
                {keypointsData || 'No data available'}
              </Box>
            </Paper>
          </CardContent>
        </Card>
      )}
    </Box>
  )
}
