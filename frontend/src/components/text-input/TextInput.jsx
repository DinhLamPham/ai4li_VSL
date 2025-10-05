/**
 * Text Input Component
 * Text input with Vietnamese language support
 *
 * USAGE:
 *   <TextInput onSubmit={handleText} placeholder="Nhập text..." />
 */
import { useState } from 'react';
import { Box, TextField, Button, Card, Typography, Chip } from '@mui/material';
import { Send, Clear } from '@mui/icons-material';

export default function TextInput({ onSubmit, placeholder, maxLength = 500, showSuggestions = false }) {
  const [text, setText] = useState('');
  const [error, setError] = useState('');

  const suggestions = [
    'Xin chào',
    'Cảm ơn bạn',
    'Tạm biệt',
    'Bạn khỏe không?',
    'Tôi tên là...',
  ];

  const handleChange = (e) => {
    const value = e.target.value;
    if (value.length <= maxLength) {
      setText(value);
      setError('');
    } else {
      setError(`Vượt quá giới hạn ${maxLength} ký tự`);
    }
  };

  const handleSubmit = () => {
    if (!text.trim()) {
      setError('Vui lòng nhập text');
      return;
    }

    onSubmit?.(text);
  };

  const handleClear = () => {
    setText('');
    setError('');
  };

  const handleSuggestionClick = (suggestion) => {
    setText(suggestion);
    setError('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <Card sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Nhập Text
      </Typography>

      <TextField
        fullWidth
        multiline
        rows={4}
        value={text}
        onChange={handleChange}
        onKeyPress={handleKeyPress}
        placeholder={placeholder || 'Nhập text tiếng Việt...'}
        error={!!error}
        helperText={error || `${text.length}/${maxLength} ký tự`}
        variant="outlined"
        sx={{ mb: 2 }}
      />

      {showSuggestions && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="caption" color="text.secondary" gutterBottom>
            Gợi ý:
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
            {suggestions.map((suggestion, index) => (
              <Chip
                key={index}
                label={suggestion}
                onClick={() => handleSuggestionClick(suggestion)}
                variant="outlined"
                size="small"
              />
            ))}
          </Box>
        </Box>
      )}

      <Box sx={{ display: 'flex', gap: 2 }}>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Send />}
          onClick={handleSubmit}
          disabled={!text.trim()}
          fullWidth
        >
          Gửi
        </Button>
        <Button
          variant="outlined"
          startIcon={<Clear />}
          onClick={handleClear}
          disabled={!text}
        >
          Xóa
        </Button>
      </Box>
    </Card>
  );
}
