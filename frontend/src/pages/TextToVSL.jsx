import { useState } from 'react'
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
  Send as SendIcon,
  ThreeDRotation as ThreeDRotationIcon,
} from '@mui/icons-material'
import TextInput from '../components/text-input/TextInput'
import VSLPlayer from '../components/vsl-player/VSLPlayer'
import { textToVSLAPI } from '../services/api'

export default function TextToVSL() {
  const [inputText, setInputText] = useState('')
  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [generateAvatar, setGenerateAvatar] = useState(false)

  const handleTranslate = async () => {
    if (!inputText.trim()) {
      setError('Vui lòng nhập text')
      return
    }

    setProcessing(true)
    setError(null)

    try {
      console.log('[TextToVSL] Translating:', inputText)
      const response = await textToVSLAPI.textToVSL(inputText)

      setResult(response.data)
      console.log('[TextToVSL] Result:', response.data)
    } catch (err) {
      console.error('[TextToVSL] Error:', err)
      setError('Lỗi khi dịch text: ' + (err.response?.data?.error || err.message))
    } finally {
      setProcessing(false)
    }
  }

  const handleGenerateAvatar = async () => {
    if (!inputText.trim()) {
      setError('Vui lòng nhập text')
      return
    }

    setProcessing(true)
    setGenerateAvatar(true)
    setError(null)

    try {
      console.log('[TextToVSL] Generating avatar for:', inputText)
      const response = await textToVSLAPI.generateAvatar(inputText)

      setResult(response.data)
      console.log('[TextToVSL] Avatar result:', response.data)
    } catch (err) {
      console.error('[TextToVSL] Error:', err)
      setError('Lỗi khi tạo avatar: ' + (err.response?.data?.error || err.message))
    } finally {
      setProcessing(false)
      setGenerateAvatar(false)
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Text → VSL
      </Typography>
      <Typography variant="body1" paragraph color="text.secondary">
        Chuyển đổi text tiếng Việt thành ngôn ngữ ký hiệu VSL
      </Typography>

      {/* Input Section */}
      <Box sx={{ mb: 3 }}>
        <TextInput
          onSubmit={(text) => {
            setInputText(text);
            handleTranslate();
          }}
          placeholder="Nhập câu tiếng Việt cần chuyển đổi sang VSL..."
          showSuggestions={true}
        />
        <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            color="secondary"
            onClick={handleGenerateAvatar}
            disabled={processing || !inputText.trim()}
            startIcon={processing && generateAvatar ? <CircularProgress size={20} /> : <ThreeDRotationIcon />}
            fullWidth
          >
            {processing && generateAvatar ? 'Đang tạo...' : 'Tạo 3D Avatar'}
          </Button>
        </Box>
      </Box>

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
              Kết quả
            </Typography>
            <Divider sx={{ mb: 2 }} />

            <Box sx={{ mb: 2 }}>
              <Chip
                label={result.success ? 'Thành công' : 'Thất bại'}
                color={result.success ? 'success' : 'error'}
                sx={{ mb: 1 }}
              />
            </Box>

            {/* Original Text */}
            <Typography variant="body1" paragraph>
              <strong>Text gốc:</strong>
            </Typography>
            <Paper elevation={0} sx={{ p: 2, bgcolor: 'grey.100', mb: 2 }}>
              <Typography>{result.original_text || inputText}</Typography>
            </Paper>

            {/* VSL Gloss */}
            {result.gloss && (
              <>
                <Typography variant="body1" paragraph>
                  <strong>VSL Gloss:</strong>
                </Typography>
                <Paper elevation={0} sx={{ p: 2, bgcolor: 'primary.light', color: 'white', mb: 2 }}>
                  <Typography variant="h6" sx={{ fontFamily: 'monospace' }}>
                    {result.gloss}
                  </Typography>
                </Paper>
              </>
            )}

            {/* 3D Avatar Animation */}
            {result.animation_url && (
              <Box sx={{ mt: 3 }}>
                <VSLPlayer
                  animationUrl={result.animation_url}
                  gloss={result.gloss}
                  onComplete={() => console.log('Animation completed')}
                />
              </Box>
            )}

            {/* Vocabulary Matches */}
            {result.vocabulary_matches && result.vocabulary_matches.length > 0 && (
              <>
                <Typography variant="body1" paragraph>
                  <strong>Từ vựng VSL matching:</strong>
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  {result.vocabulary_matches.map((word, index) => (
                    <Chip key={index} label={word} variant="outlined" />
                  ))}
                </Box>
              </>
            )}

            {result.confidence !== undefined && (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                Độ tin cậy: {(result.confidence * 100).toFixed(1)}%
              </Typography>
            )}
          </CardContent>
        </Card>
      )}

      {/* Info Section */}
      <Alert severity="info" sx={{ mt: 3 }}>
        <Typography variant="body2">
          <strong>Về VSL Gloss:</strong> VSL Gloss là ký hiệu dùng để ghi chép ngôn ngữ ký hiệu.
          Các từ được viết HOA, sử dụng dấu gạch nối (-) cho các từ ghép, và có thêm các markers
          như QUESTION?, TIME-PAST, v.v.
        </Typography>
      </Alert>
    </Box>
  )
}
