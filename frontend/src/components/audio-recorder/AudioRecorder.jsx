/**
 * Audio Recorder Component
 * Record audio for speech-to-text conversion
 *
 * USAGE:
 *   <AudioRecorder onRecordingComplete={handleAudio} />
 */
import { useState, useRef } from 'react';
import { Box, Button, Card, Typography, LinearProgress, Alert } from '@mui/material';
import { Mic, Stop, PlayArrow } from '@mui/icons-material';

export default function AudioRecorder({ onRecordingComplete, onError }) {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioURL, setAudioURL] = useState(null);
  const [duration, setDuration] = useState(0);
  const [error, setError] = useState(null);

  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const timerRef = useRef(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      mediaRecorderRef.current = new MediaRecorder(stream);
      chunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        const url = URL.createObjectURL(blob);

        setAudioBlob(blob);
        setAudioURL(url);

        // Call callback
        onRecordingComplete?.(blob, url);

        // Stop timer
        if (timerRef.current) {
          clearInterval(timerRef.current);
        }

        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setDuration(0);
      setError(null);

      // Start timer
      timerRef.current = setInterval(() => {
        setDuration(prev => prev + 1);
      }, 1000);

    } catch (err) {
      console.error('Recording error:', err);
      setError('Không thể truy cập microphone. Vui lòng kiểm tra quyền truy cập.');
      onError?.(err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const playAudio = () => {
    if (audioURL) {
      const audio = new Audio(audioURL);
      audio.play();
    }
  };

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <Card sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Audio Recorder
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ textAlign: 'center', my: 3 }}>
        {isRecording && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="h4" color="error">
              {formatDuration(duration)}
            </Typography>
            <LinearProgress color="error" sx={{ mt: 1 }} />
          </Box>
        )}

        {!isRecording && audioURL && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="body1" color="success.main">
              Đã ghi âm: {formatDuration(duration)}
            </Typography>
          </Box>
        )}

        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
          {!isRecording ? (
            <Button
              variant="contained"
              color="primary"
              size="large"
              startIcon={<Mic />}
              onClick={startRecording}
            >
              Bắt đầu ghi âm
            </Button>
          ) : (
            <Button
              variant="contained"
              color="error"
              size="large"
              startIcon={<Stop />}
              onClick={stopRecording}
            >
              Dừng ghi âm
            </Button>
          )}

          {audioURL && !isRecording && (
            <Button
              variant="outlined"
              startIcon={<PlayArrow />}
              onClick={playAudio}
            >
              Phát lại
            </Button>
          )}
        </Box>
      </Box>
    </Card>
  );
}
