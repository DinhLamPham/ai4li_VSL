import { useState } from 'react'
import {
  Box,
  Typography,
  Paper,
  Tabs,
  Tab,
  Button,
  TextField,
  Alert,
  Card,
  CardContent,
  Divider,
} from '@mui/material'
import {
  DataUsage as DataUsageIcon,
  ModelTraining as ModelTrainingIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material'

function TabPanel({ children, value, index }) {
  return (
    <div role="tabpanel" hidden={value !== index}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  )
}

export default function Tools() {
  const [tabValue, setTabValue] = useState(0)

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue)
  }

  const handleDataAugmentation = () => {
    console.log('[Tools] Data Augmentation clicked')
    alert('Chức năng đang được phát triển bởi nhóm Data & Tools')
  }

  const handleModelUpload = () => {
    console.log('[Tools] Model Upload clicked')
    alert('Chức năng đang được phát triển bởi nhóm Data & Tools')
  }

  const handleBenchmark = () => {
    console.log('[Tools] Benchmark clicked')
    alert('Chức năng đang được phát triển bởi nhóm Data & Tools')
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Tools
      </Typography>
      <Typography variant="body1" paragraph color="text.secondary">
        Công cụ hỗ trợ phát triển và testing
      </Typography>

      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          variant="fullWidth"
          aria-label="tools tabs"
        >
          <Tab icon={<DataUsageIcon />} label="Data Augmentation" />
          <Tab icon={<ModelTrainingIcon />} label="Model Management" />
          <Tab icon={<AssessmentIcon />} label="Testing & Benchmark" />
        </Tabs>
      </Paper>

      {/* Data Augmentation Tab */}
      <TabPanel value={tabValue} index={0}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Data Augmentation
            </Typography>
            <Divider sx={{ mb: 2 }} />

            <Typography variant="body2" paragraph>
              Tăng cường dữ liệu training bằng các kỹ thuật augmentation
            </Typography>

            <TextField
              fullWidth
              label="Data Directory"
              placeholder="/path/to/data"
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              select
              label="Data Type"
              SelectProps={{ native: true }}
              sx={{ mb: 2 }}
            >
              <option value="video">Video</option>
              <option value="image">Image</option>
              <option value="audio">Audio</option>
            </TextField>

            <Button
              variant="contained"
              onClick={handleDataAugmentation}
              fullWidth
            >
              Start Augmentation
            </Button>

            <Alert severity="info" sx={{ mt: 2 }}>
              Chức năng đang được phát triển bởi <strong>Group 4: Data & Tools Team</strong>
            </Alert>
          </CardContent>
        </Card>
      </TabPanel>

      {/* Model Management Tab */}
      <TabPanel value={tabValue} index={1}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Model Management
            </Typography>
            <Divider sx={{ mb: 2 }} />

            <Typography variant="body2" paragraph>
              Quản lý trained models: upload, download, activate
            </Typography>

            <TextField
              fullWidth
              label="Model Name"
              placeholder="vsl_gesture_recognizer"
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              label="Model Version"
              placeholder="v1.0.0"
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              select
              label="Model Type"
              SelectProps={{ native: true }}
              sx={{ mb: 2 }}
            >
              <option value="vsl_recognition">VSL Recognition</option>
              <option value="gesture">Gesture</option>
              <option value="emotion">Emotion</option>
              <option value="stt">Speech-to-Text</option>
              <option value="tts">Text-to-Speech</option>
            </TextField>

            <Button
              variant="contained"
              onClick={handleModelUpload}
              fullWidth
            >
              Upload Model
            </Button>

            <Alert severity="info" sx={{ mt: 2 }}>
              Chức năng đang được phát triển bởi <strong>Group 4: Data & Tools Team</strong>
            </Alert>
          </CardContent>
        </Card>
      </TabPanel>

      {/* Testing & Benchmark Tab */}
      <TabPanel value={tabValue} index={2}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Testing & Benchmark
            </Typography>
            <Divider sx={{ mb: 2 }} />

            <Typography variant="body2" paragraph>
              Đánh giá hiệu năng model trên test dataset
            </Typography>

            <TextField
              fullWidth
              label="Model Path"
              placeholder="/path/to/model.h5"
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              label="Test Data Directory"
              placeholder="/path/to/test_data"
              sx={{ mb: 2 }}
            />

            <Button
              variant="contained"
              onClick={handleBenchmark}
              fullWidth
            >
              Run Benchmark
            </Button>

            <Alert severity="info" sx={{ mt: 2 }}>
              Chức năng đang được phát triển bởi <strong>Group 4: Data & Tools Team</strong>
            </Alert>
          </CardContent>
        </Card>
      </TabPanel>

      {/* General Info */}
      <Paper sx={{ p: 3, mt: 3, bgcolor: 'grey.50' }}>
        <Typography variant="h6" gutterBottom>
          Hướng dẫn cho sinh viên
        </Typography>
        <Typography variant="body2" paragraph>
          <strong>Nhóm 4 - Data & Tools Team:</strong>
        </Typography>
        <Typography variant="body2" component="div">
          <ul>
            <li>Implement data augmentation functions trong <code>backend/app/modules/data_tools/augmentation.py</code></li>
            <li>Implement model management trong <code>backend/app/core/trained_model_registry.py</code></li>
            <li>Implement testing tools trong <code>backend/app/modules/data_tools/custom_tools.py</code></li>
            <li>Connect frontend với backend APIs</li>
          </ul>
        </Typography>
      </Paper>
    </Box>
  )
}
