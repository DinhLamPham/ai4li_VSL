/**
 * VSL Player Component
 * 3D Avatar player for displaying VSL signs
 *
 * USAGE:
 *   <VSLPlayer animationUrl="/path/to/animation.mp4" />
 *
 * STUDENT TODO:
 *   - Integrate Three.js for 3D avatar rendering
 *   - Load and play animation sequences
 *   - Add playback controls
 */
import { useState, useRef, useEffect } from 'react';
import { Box, Card, Typography, Button, Slider, IconButton } from '@mui/material';
import { PlayArrow, Pause, Replay, Speed } from '@mui/icons-material';

export default function VSLPlayer({ animationUrl, gloss, onComplete }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [speed, setSpeed] = useState(1.0);
  const [loading, setLoading] = useState(false);
  const videoRef = useRef(null);

  useEffect(() => {
    if (animationUrl) {
      setLoading(true);
      // STUDENT TODO: Load 3D animation or video
      setTimeout(() => setLoading(false), 500);
    }
  }, [animationUrl]);

  const handlePlay = () => {
    if (videoRef.current) {
      videoRef.current.play();
      setIsPlaying(true);
    }
  };

  const handlePause = () => {
    if (videoRef.current) {
      videoRef.current.pause();
      setIsPlaying(false);
    }
  };

  const handleReplay = () => {
    if (videoRef.current) {
      videoRef.current.currentTime = 0;
      videoRef.current.play();
      setIsPlaying(true);
    }
  };

  const handleSpeedChange = (newSpeed) => {
    setSpeed(newSpeed);
    if (videoRef.current) {
      videoRef.current.playbackRate = newSpeed;
    }
  };

  const handleProgress = () => {
    if (videoRef.current) {
      const progress = (videoRef.current.currentTime / videoRef.current.duration) * 100;
      setProgress(progress || 0);
    }
  };

  const handleEnded = () => {
    setIsPlaying(false);
    onComplete?.();
  };

  return (
    <Card sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        VSL 3D Avatar Player
      </Typography>

      {gloss && (
        <Box sx={{ mb: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
          <Typography variant="caption" color="text.secondary">
            VSL Gloss:
          </Typography>
          <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
            {gloss}
          </Typography>
        </Box>
      )}

      <Box sx={{
        position: 'relative',
        width: '100%',
        height: 400,
        bgcolor: 'grey.900',
        borderRadius: 2,
        overflow: 'hidden',
        mb: 2,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        {loading ? (
          <Typography color="white">Loading animation...</Typography>
        ) : animationUrl ? (
          // If video URL provided, show video player
          // STUDENT TODO: Replace with Three.js 3D avatar
          <video
            ref={videoRef}
            style={{ width: '100%', height: '100%', objectFit: 'contain' }}
            onTimeUpdate={handleProgress}
            onEnded={handleEnded}
          >
            <source src={animationUrl} type="video/mp4" />
          </video>
        ) : (
          <Box sx={{ textAlign: 'center', color: 'white', p: 3 }}>
            <Typography variant="h6" gutterBottom>
              3D Avatar Placeholder
            </Typography>
            <Typography variant="body2" color="grey.400">
              STUDENT TODO: Integrate Three.js here
            </Typography>
            <Typography variant="caption" color="grey.500" sx={{ mt: 1, display: 'block' }}>
              Libraries: @react-three/fiber, @react-three/drei, three
            </Typography>
          </Box>
        )}
      </Box>

      {/* Progress Bar */}
      <Slider
        value={progress}
        onChange={(e, value) => {
          if (videoRef.current) {
            videoRef.current.currentTime = (value / 100) * videoRef.current.duration;
          }
        }}
        sx={{ mb: 1 }}
      />

      {/* Controls */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 2 }}>
        {!isPlaying ? (
          <IconButton color="primary" onClick={handlePlay} size="large">
            <PlayArrow fontSize="large" />
          </IconButton>
        ) : (
          <IconButton color="primary" onClick={handlePause} size="large">
            <Pause fontSize="large" />
          </IconButton>
        )}

        <IconButton onClick={handleReplay}>
          <Replay />
        </IconButton>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Speed />
          <Button
            size="small"
            variant={speed === 0.5 ? 'contained' : 'outlined'}
            onClick={() => handleSpeedChange(0.5)}
          >
            0.5x
          </Button>
          <Button
            size="small"
            variant={speed === 1.0 ? 'contained' : 'outlined'}
            onClick={() => handleSpeedChange(1.0)}
          >
            1x
          </Button>
          <Button
            size="small"
            variant={speed === 1.5 ? 'contained' : 'outlined'}
            onClick={() => handleSpeedChange(1.5)}
          >
            1.5x
          </Button>
        </Box>
      </Box>
    </Card>
  );
}
