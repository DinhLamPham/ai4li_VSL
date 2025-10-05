import { Box, Typography, Grid, Card, CardContent, CardActions, Button, Paper } from '@mui/material'
import { useNavigate } from 'react-router-dom'
import {
  Videocam as VideocamIcon,
  Mic as MicIcon,
  TextFields as TextFieldsIcon,
  Build as BuildIcon,
} from '@mui/icons-material'

export default function Home() {
  const navigate = useNavigate()

  const features = [
    {
      title: 'Camera → Text',
      description: 'Nhận diện ngôn ngữ ký hiệu VSL từ camera hoặc video và chuyển thành text',
      icon: <VideocamIcon sx={{ fontSize: 60 }} />,
      path: '/camera-to-text',
      color: '#1976d2',
    },
    {
      title: 'Audio → Text',
      description: 'Chuyển đổi giọng nói thành text (Speech-to-Text)',
      icon: <MicIcon sx={{ fontSize: 60 }} />,
      path: '/audio-to-text',
      color: '#dc004e',
    },
    {
      title: 'Text → VSL',
      description: 'Chuyển đổi text tiếng Việt thành ngôn ngữ ký hiệu VSL với 3D Avatar',
      icon: <TextFieldsIcon sx={{ fontSize: 60 }} />,
      path: '/text-to-vsl',
      color: '#388e3c',
    },
    {
      title: 'Tools',
      description: 'Công cụ hỗ trợ: Data augmentation, Model management, Testing',
      icon: <BuildIcon sx={{ fontSize: 60 }} />,
      path: '/tools',
      color: '#f57c00',
    },
  ]

  return (
    <Box>
      <Paper elevation={3} sx={{ p: 4, mb: 4, textAlign: 'center', bgcolor: 'primary.main', color: 'white' }}>
        <Typography variant="h3" component="h1" gutterBottom>
          VSL Application
        </Typography>
        <Typography variant="h6">
          Ứng dụng AI hỗ trợ người khiếm thính giao tiếp qua ngôn ngữ ký hiệu Việt Nam
        </Typography>
      </Paper>

      <Grid container spacing={3}>
        {features.map((feature) => (
          <Grid item xs={12} sm={6} md={6} key={feature.title}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                },
              }}
            >
              <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                <Box sx={{ color: feature.color, mb: 2 }}>
                  {feature.icon}
                </Box>
                <Typography gutterBottom variant="h5" component="h2">
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
              <CardActions sx={{ justifyContent: 'center', pb: 2 }}>
                <Button
                  size="large"
                  variant="contained"
                  onClick={() => navigate(feature.path)}
                  sx={{ bgcolor: feature.color }}
                >
                  Sử dụng
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Paper elevation={2} sx={{ p: 3, mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Về dự án
        </Typography>
        <Typography variant="body1" paragraph>
          VSL Application là dự án ứng dụng AI được xây dựng bởi AI4LI.org, nhằm hỗ trợ
          người khiếm thính giao tiếp hiệu quả hơn thông qua công nghệ nhận diện và dịch
          ngôn ngữ ký hiệu Việt Nam (VSL).
        </Typography>
        <Typography variant="body2" color="text.secondary">
          <strong>Công nghệ sử dụng:</strong> React, FastAPI, MediaPipe, TensorFlow, Three.js
        </Typography>
      </Paper>
    </Box>
  )
}
