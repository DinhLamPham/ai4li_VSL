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
  Mic as MicIcon,
  CloudUpload as CloudUploadIcon,
  Stop as StopIcon,
} from '@mui/icons-material'
import AudioRecorder from '../components/audio-recorder/AudioRecorder'
import { speechAPI } from '../services/api'

export default function AudioToText() {
  const [mode, setMode] = useState('upload') // 'upload' or 'record'
  const [isRecording, setIsRecording] = useState(false)
  const [audioFile, setAudioFile] = useState(null)
  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const fileInputRef = useRef(null)

  const handleFileUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
      setAudioFile(file)
      setResult(null)
      setError(null)
    }
  }

  const handleProcessAudio = async () => {
    if (!audioFile) {
      setError('Vui lòng chọn audio file')
      return
    }

    setProcessing(true)
    setError(null)

    try {
      console.log('[AudioToText] Processing audio:', audioFile.name)
      const response = await speechAPI.audioToText(audioFile)

      setResult(response.data)
      console.log('[AudioToText] Result:', response.data)
    } catch (err) {
      console.error('[AudioToText] Error:', err)
      setError('Lỗi khi xử lý audio: ' + (err.response?.data?.error || err.message))
    } finally {
      setProcessing(false)
    }
  }

  const handleRecord = () => {
    // TODO: Implement audio recording
    console.log('[AudioToText] Record clicked')
    alert('Chức năng ghi âm đang được phát triển')
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Audio → Text
      </Typography>
      <Typography variant="body1" paragraph color="text.secondary">
        Chuyển đổi giọng nói thành text (Speech-to-Text)
      </Typography>

      {/* Mode Selection */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
          <Button
            variant={mode === 'upload' ? 'contained' : 'outlined'}
            onClick={() => setMode('upload')}
            startIcon={<CloudUploadIcon />}
          >
            Upload Audio
          </Button>
          <Button
            variant={mode === 'record' ? 'contained' : 'outlined'}
            onClick={() => setMode('record')}
            startIcon={<MicIcon />}
          >
            Ghi âm
          </Button>
        </Box>
      </Paper>

      {/* Upload Mode */}
      {mode === 'upload' && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Upload Audio File
          </Typography>

          <Box sx={{ mb: 2 }}>
            <input
              ref={fileInputRef}
              type="file"
              accept="audio/*"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
            <Button
              variant="contained"
              onClick={() => fileInputRef.current?.click()}
              startIcon={<CloudUploadIcon />}
            >
              Chọn Audio
            </Button>
          </Box>

          {audioFile && (
            <Alert severity="info" sx={{ mb: 2 }}>
              Đã chọn: {audioFile.name} ({(audioFile.size / 1024 / 1024).toFixed(2)} MB)
            </Alert>
          )}

          <Button
            variant="contained"
            color="primary"
            onClick={handleProcessAudio}
            disabled={!audioFile || processing}
            fullWidth
            sx={{ mt: 2 }}
          >
            {processing ? (
              <>
                <CircularProgress size={24} sx={{ mr: 1 }} />
                Đang xử lý...
              </>
            ) : (
              'Chuyển đổi thành Text'
            )}
          </Button>
        </Paper>
      )}

      {/* Record Mode */}
      {mode === 'record' && (
        <Box sx={{ mb: 3 }}>
          <AudioRecorder
            onRecordingComplete={async (audioBlob, audioURL) => {
              console.log('Recording complete');
              setAudioFile(audioBlob);
              // Auto-process
              setProcessing(true);
              try {
                const response = await speechAPI.audioToText(audioBlob);
                setResult(response.data);
              } catch (err) {
                setError('Lỗi khi xử lý audio: ' + (err.response?.data?.error || err.message));
              } finally {
                setProcessing(false);
              }
            }}
            onError={(err) => {
              setError('Lỗi ghi âm: ' + err.message);
            }}
          />
          <Alert severity="info" sx={{ mt: 2 }}>
            Chức năng ghi âm đang được phát triển bởi sinh viên
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
              Kết quả chuyển đổi
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
              <strong>Text nhận dạng:</strong>
            </Typography>
            <Paper elevation={0} sx={{ p: 2, bgcolor: 'grey.100', mb: 2 }}>
              <Typography variant="h6">
                {result.text || 'Không nhận dạng được'}
              </Typography>
            </Paper>

            {result.confidence !== undefined && (
              <Typography variant="body2" color="text.secondary" paragraph>
                Độ tin cậy: {(result.confidence * 100).toFixed(1)}%
              </Typography>
            )}

            {result.language && (
              <Typography variant="body2" color="text.secondary" paragraph>
                Ngôn ngữ: {result.language}
              </Typography>
            )}

            {result.processing_time !== undefined && (
              <Typography variant="body2" color="text.secondary">
                Thời gian xử lý: {result.processing_time.toFixed(2)}s
              </Typography>
            )}
          </CardContent>
        </Card>
      )}
    </Box>
  )
}
