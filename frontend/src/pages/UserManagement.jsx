import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Chip,
  Alert,
  InputAdornment,
  FormControl,
  InputLabel,
  Select,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility,
  VisibilityOff,
  Refresh as RefreshIcon,
  CheckCircle,
  Block,
} from '@mui/icons-material';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function UserManagement() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [showPassword, setShowPassword] = useState(false);
  const [includeDisabled, setIncludeDisabled] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    role: 'user',
  });

  // Fetch users
  const fetchUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(
        `${API_URL}/api/v1/users?include_disabled=${includeDisabled}`
      );

      // Check if response has expected structure
      if (response.data && response.data.data && response.data.data.users) {
        setUsers(response.data.data.users);
      } else {
        console.error('Unexpected response structure:', response.data);
        setUsers([]);
        setError('Unexpected response format from server');
      }
    } catch (err) {
      console.error('Failed to fetch users:', err);
      setError('Failed to fetch users: ' + (err.response?.data?.message || err.message));
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [includeDisabled]);

  // Handle form change
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Open create dialog
  const handleCreate = () => {
    setEditMode(false);
    setCurrentUser(null);
    setFormData({
      username: '',
      email: '',
      password: '',
      full_name: '',
      role: 'user',
    });
    setOpenDialog(true);
  };

  // Open edit dialog
  const handleEdit = (user) => {
    setEditMode(true);
    setCurrentUser(user);
    setFormData({
      username: user.username,
      email: user.email || '',
      password: '',
      full_name: user.full_name || '',
      role: user.role || 'user',
    });
    setOpenDialog(true);
  };

  // Handle submit
  const handleSubmit = async () => {
    setError(null);
    setSuccess(null);

    try {
      if (editMode && currentUser) {
        // Update user
        const params = new URLSearchParams();
        if (formData.username !== currentUser.username) params.append('username', formData.username);
        if (formData.email) params.append('email', formData.email);
        if (formData.password) params.append('password', formData.password);
        if (formData.full_name) params.append('full_name', formData.full_name);
        if (formData.role) params.append('role', formData.role);

        await axios.put(`${API_URL}/api/v1/users/${currentUser.id}?${params.toString()}`);
        setSuccess(`User "${formData.username}" updated successfully`);
      } else {
        // Create user
        await axios.post(`${API_URL}/api/v1/users`, formData);
        setSuccess(`User "${formData.username}" created successfully`);
      }

      setOpenDialog(false);
      fetchUsers();
    } catch (err) {
      setError(err.response?.data?.message || err.message);
    }
  };

  // Handle disable
  const handleDisable = async (user) => {
    if (!confirm(`Are you sure you want to disable user "${user.username}"?`)) return;

    try {
      await axios.delete(`${API_URL}/api/v1/users/${user.id}`);
      setSuccess(`User "${user.username}" disabled`);
      fetchUsers();
    } catch (err) {
      setError(err.response?.data?.message || err.message);
    }
  };

  // Handle enable
  const handleEnable = async (user) => {
    try {
      await axios.post(`${API_URL}/api/v1/users/${user.id}/enable`);
      setSuccess(`User "${user.username}" enabled`);
      fetchUsers();
    } catch (err) {
      setError(err.response?.data?.message || err.message);
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">User Management</Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControlLabel
            control={
              <Switch
                checked={includeDisabled}
                onChange={(e) => setIncludeDisabled(e.target.checked)}
              />
            }
            label="Show disabled"
          />
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={fetchUsers}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleCreate}
          >
            Add User
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Username</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Full Name</TableCell>
              <TableCell>Role</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Created</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.id}</TableCell>
                <TableCell>
                  <strong>{user.username}</strong>
                </TableCell>
                <TableCell>{user.email || '-'}</TableCell>
                <TableCell>{user.full_name || '-'}</TableCell>
                <TableCell>
                  <Chip
                    label={user.role}
                    size="small"
                    color={user.role === 'admin' ? 'error' : 'default'}
                  />
                </TableCell>
                <TableCell>
                  {user.is_active ? (
                    <Chip
                      icon={<CheckCircle />}
                      label="Active"
                      size="small"
                      color="success"
                    />
                  ) : (
                    <Chip
                      icon={<Block />}
                      label="Disabled"
                      size="small"
                      color="default"
                    />
                  )}
                </TableCell>
                <TableCell>
                  {new Date(user.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    size="small"
                    color="primary"
                    onClick={() => handleEdit(user)}
                  >
                    <EditIcon />
                  </IconButton>
                  {user.is_active ? (
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => handleDisable(user)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  ) : (
                    <IconButton
                      size="small"
                      color="success"
                      onClick={() => handleEnable(user)}
                      title="Enable user"
                    >
                      <CheckCircle />
                    </IconButton>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Add/Edit Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editMode ? 'Edit User' : 'Create New User'}</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              fullWidth
            />
            <TextField
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              fullWidth
            />
            <TextField
              label={editMode ? 'Password (leave empty to keep current)' : 'Password'}
              name="password"
              type={showPassword ? 'text' : 'password'}
              value={formData.password}
              onChange={handleChange}
              required={!editMode}
              fullWidth
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              helperText="POC: Plain text password for easy access"
            />
            <TextField
              label="Full Name"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              fullWidth
            />
            <FormControl fullWidth>
              <InputLabel>Role</InputLabel>
              <Select
                name="role"
                value={formData.role}
                onChange={handleChange}
                label="Role"
              >
                <MenuItem value="admin">Admin</MenuItem>
                <MenuItem value="user">User</MenuItem>
                <MenuItem value="student">Student</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={!formData.username || (!editMode && !formData.password)}
          >
            {editMode ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
