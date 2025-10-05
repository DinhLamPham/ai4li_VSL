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

    try {
      console.log('[CameraToText] Processing video:', videoFile.name)
      const response = await vslRecognitionAPI.recognizeVideo(videoFile)

      setResult(response.data)
      console.log('[CameraToText] Result:', response.data)
    } catch (err) {
      console.error('[CameraToText] Error:', err)
      setError('Lỗi khi xử lý video: ' + (err.response?.data?.error || err.message))
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
              Kết quả nhận diện
            </Typography>
            <Divider sx={{ mb: 2 }} />

            <Box sx={{ mb: 2 }}>
              <Chip
                label={result.success ? 'Thành công' : 'Thất bại'}
                color={result.success ? 'success' : 'error'}
                sx={{ mb: 1 }}
              />
            </Box>

            <Typography variant="body1" paragraph>
              <strong>Text nhận diện:</strong>
            </Typography>
            <Paper elevation={0} sx={{ p: 2, bgcolor: 'grey.100', mb: 2 }}>
              <Typography variant="h6">
                {result.detected_text || 'Không nhận diện được'}
              </Typography>
            </Paper>

            {result.confidence !== undefined && (
              <Typography variant="body2" color="text.secondary">
                Độ tin cậy: {(result.confidence * 100).toFixed(1)}%
              </Typography>
            )}

            {result.processing_time !== undefined && (
              <Typography variant="body2" color="text.secondary">
                Thời gian xử lý: {result.processing_time.toFixed(2)}s
              </Typography>
            )}

            {result.frame_count !== undefined && (
              <Typography variant="body2" color="text.secondary">
                Số frames đã xử lý: {result.frame_count}
              </Typography>
            )}
          </CardContent>
        </Card>
      )}
    </Box>
  )
}
