import { Routes, Route } from 'react-router-dom'
import { Box } from '@mui/material'
import Layout from './components/common/Layout'
import Home from './pages/Home'
import CameraToText from './pages/CameraToText'
import AudioToText from './pages/AudioToText'
import TextToVSL from './pages/TextToVSL'
import Tools from './pages/Tools'
import UserManagement from './pages/UserManagement'

function App() {
  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="camera-to-text" element={<CameraToText />} />
          <Route path="audio-to-text" element={<AudioToText />} />
          <Route path="text-to-vsl" element={<TextToVSL />} />
          <Route path="tools" element={<Tools />} />
          <Route path="users" element={<UserManagement />} />
        </Route>
      </Routes>
    </Box>
  )
}

export default App
