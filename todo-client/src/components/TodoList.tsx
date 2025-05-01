import React, { useState, useEffect } from 'react';
import { 
    List, ListItem, ListItemText, ListItemSecondaryAction,
    IconButton, Checkbox, TextField, Button, Box, Paper,
    Select, MenuItem, FormControl, InputLabel,
    Chip, Stack, Typography, SelectChangeEvent,
    Alert, Snackbar, Dialog, DialogTitle,
    DialogContent, DialogActions, Container,
    Switch, FormControlLabel, Menu
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import axios, { AxiosError } from 'axios';
import { Todo, categories } from '../types/Todo';

const API_BASE_URL = 'http://localhost:5141/api';

interface TodoListProps {
    darkMode: boolean;
    setDarkMode: (darkMode: boolean) => void;
    token: string;
    username: string;
    onLogout: () => void;
}

const getErrorMessage = (error: unknown) => {
    if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError<{ error?: string; details?: string }>;
        if (axiosError.response?.data) {
            return axiosError.response.data.details || axiosError.response.data.error || axiosError.message;
        }
        return axiosError.message;
    }
    return 'An unexpected error occurred';
};

export const TodoList = ({ darkMode, setDarkMode, token, username, onLogout }: TodoListProps) => {
    const [todos, setTodos] = useState<Todo[]>([]);
    const [newTodo, setNewTodo] = useState('');
    const [selectedCategory, setSelectedCategory] = useState<string>('Work');
    const [filterCategory, setFilterCategory] = useState<string>('all');
    const [error, setError] = useState<string | null>(null);
    const [menuAnchorEl, setMenuAnchorEl] = useState<null | HTMLElement>(null);
    const [importDialogOpen, setImportDialogOpen] = useState(false);
    const [importData, setImportData] = useState('');
    
    // Edit mode state
    const [editDialogOpen, setEditDialogOpen] = useState(false);
    const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
    const [editTitle, setEditTitle] = useState('');
    const [editCategory, setEditCategory] = useState('');

    useEffect(() => {
        const fetchTodos = async () => {
            try {
                const response = await axios.get(`${API_BASE_URL}/todo`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
                console.log('API Response:', response.data);
                setTodos(response.data);
                setError(null);
            } catch (error: unknown) {
                if (axios.isAxiosError(error)) {
                    console.error('Full error object:', error);
                    console.error('Error status:', error.response?.status);
                    console.error('Error data:', error.response?.data);
                    const errorMessage = getErrorMessage(error);
                    console.error('Error details:', error);
                    setError(`Failed to fetch todos: ${errorMessage}`);
                } else {
                    console.error('Unexpected error:', error);
                    setError('An unexpected error occurred');
                }
            }
        };
        fetchTodos();
    }, [token]);

    const addTodo = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!newTodo.trim()) return;

        try {
            const response = await axios.post(`${API_BASE_URL}/todo`, {
                title: newTodo,
                isCompleted: false,
                category: selectedCategory
            }, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            console.log('Add todo response:', response.data);
            setNewTodo('');
            setTodos([...todos, response.data]);
            setError(null);
        } catch (error: unknown) {
            if (axios.isAxiosError(error)) {
                const errorMessage = getErrorMessage(error);
                console.error('Error adding todo:', error);
                setError(`Failed to add todo: ${errorMessage}`);
            } else {
                console.error('Unexpected error:', error);
                setError('An unexpected error occurred');
            }
        }
    };

    const toggleTodo = async (todo: Todo) => {
        try {
            const response = await axios.put(`${API_BASE_URL}/todo/${todo.id}`, {
                ...todo,
                isCompleted: !todo.isCompleted
            }, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            setTodos(todos.map(t => t.id === todo.id ? response.data : t));
            setError(null);
        } catch (error: unknown) {
            if (axios.isAxiosError(error)) {
                const errorMessage = getErrorMessage(error);
                console.error('Error updating todo:', error);
                setError(`Failed to update todo: ${errorMessage}`);
            } else {
                console.error('Unexpected error:', error);
                setError('An unexpected error occurred');
            }
        }
    };

    const deleteTodo = async (id: number) => {
        try {
            await axios.delete(`${API_BASE_URL}/todo/${id}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            setTodos(todos.filter(t => t.id !== id));
            setError(null);
        } catch (error: unknown) {
            if (axios.isAxiosError(error)) {
                const errorMessage = getErrorMessage(error);
                console.error('Error deleting todo:', error);
                setError(`Failed to delete todo: ${errorMessage}`);
            } else {
                console.error('Unexpected error:', error);
                setError('An unexpected error occurred');
            }
        }
    };

    const handleCategoryChange = (event: SelectChangeEvent) => {
        setSelectedCategory(event.target.value);
    };

    // Edit functionality
    const openEditDialog = (todo: Todo) => {
        setEditingTodo(todo);
        setEditTitle(todo.title);
        setEditCategory(todo.category);
        setEditDialogOpen(true);
    };

    const closeEditDialog = () => {
        setEditDialogOpen(false);
        setEditingTodo(null);
        setEditTitle('');
        setEditCategory('');
    };

    const handleEditSubmit = async () => {
        if (!editingTodo || !editTitle.trim()) return;

        try {
            await axios.put(`${API_BASE_URL}/todo/${editingTodo.id}`, {
                ...editingTodo,
                title: editTitle,
                category: editCategory
            }, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            setTodos(todos.map(t => t.id === editingTodo.id ? { ...editingTodo, title: editTitle, category: editCategory } : t));
            closeEditDialog();
            setError(null);
        } catch (error: unknown) {
            if (axios.isAxiosError(error)) {
                const errorMessage = getErrorMessage(error);
                console.error('Error updating todo:', error);
                setError(`Failed to update todo: ${errorMessage}`);
            } else {
                console.error('Unexpected error:', error);
                setError('An unexpected error occurred');
            }
        }
    };

    const filteredTodos = filterCategory === 'all' 
        ? todos
        : todos.filter(todo => todo.category === filterCategory);

    const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
        setMenuAnchorEl(event.currentTarget);
    };

    const handleMenuClose = () => {
        setMenuAnchorEl(null);
    };

    const exportToJson = () => {
        const dataStr = JSON.stringify(todos, null, 2);
        downloadFile(dataStr, 'todos.json', 'application/json');
        handleMenuClose();
    };

    const exportToCsv = () => {
        const headers = ['id', 'title', 'category', 'isCompleted', 'createdAt'];
        const csvContent = [
            headers.join(','),
            ...todos.map(todo => [
                todo.id,
                `"${todo.title.replace(/"/g, '""')}"`,
                todo.category,
                todo.isCompleted,
                todo.createdAt
            ].join(','))
        ].join('\n');
        downloadFile(csvContent, 'todos.csv', 'text/csv');
        handleMenuClose();
    };

    const downloadFile = (content: string, fileName: string, contentType: string) => {
        const blob = new Blob([content], { type: contentType });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };

    const handleImportDialogOpen = () => {
        setImportDialogOpen(true);
        handleMenuClose();
    };

    const handleImportDialogClose = () => {
        setImportDialogOpen(false);
        setImportData('');
    };

    const handleImport = async () => {
        try {
            let importedTodos: Todo[];
            try {
                // Try parsing as JSON first
                importedTodos = JSON.parse(importData);
            } catch {
                // If JSON parsing fails, try CSV
                importedTodos = parseCsv(importData);
            }

            // Validate and import each todo
            for (const todo of importedTodos) {
                await axios.post(`${API_BASE_URL}/todo`, {
                    title: todo.title,
                    category: todo.category,
                    isCompleted: todo.isCompleted
                }, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
            }

            setTodos([...todos, ...importedTodos]);
            handleImportDialogClose();
            setError(null);
        } catch (error: unknown) {
            if (axios.isAxiosError(error)) {
                const errorMessage = getErrorMessage(error);
                setError(`Failed to import todos: ${errorMessage}`);
            } else {
                console.error('Unexpected error:', error);
                setError('An unexpected error occurred');
            }
        }
    };

    const parseCsv = (csvContent: string): Todo[] => {
        const lines = csvContent.split('\n');
        const headers = lines[0].toLowerCase().split(',');
        
        return lines.slice(1).map(line => {
            const values = line.split(',');
            const todo: any = {};
            headers.forEach((header, index) => {
                if (header === 'iscompleted') {
                    todo.isCompleted = values[index].toLowerCase() === 'true';
                } else {
                    todo[header] = values[index].replace(/^"(.*)"$/, '$1');
                }
            });
            return todo;
        });
    };

    return (
        <Container maxWidth="md" sx={{ mt: 4 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h4" component="h1">
                    Welcome, {username}
                </Typography>
                <Box sx={{ display: 'flex', gap: 2 }}>
                    <FormControlLabel
                        control={
                            <Switch
                                checked={darkMode}
                                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setDarkMode(e.target.checked)}
                                icon={<LightModeIcon />}
                                checkedIcon={<DarkModeIcon />}
                            />
                        }
                        label={darkMode ? "Dark Mode" : "Light Mode"}
                    />
                    <Button
                        variant="outlined"
                        color="primary"
                        onClick={onLogout}
                    >
                        Logout
                    </Button>
                </Box>
            </Box>

            <Box sx={{ maxWidth: 800, margin: 'auto', mt: 4, p: 2 }}>
                <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                    <IconButton onClick={handleMenuOpen}>
                        <MoreVertIcon />
                    </IconButton>
                </Stack>

                <Menu
                    anchorEl={menuAnchorEl}
                    open={Boolean(menuAnchorEl)}
                    onClose={handleMenuClose}
                >
                    <MenuItem onClick={exportToJson}>
                        <FileDownloadIcon sx={{ mr: 1 }} />
                        Export as JSON
                    </MenuItem>
                    <MenuItem onClick={exportToCsv}>
                        <FileDownloadIcon sx={{ mr: 1 }} />
                        Export as CSV
                    </MenuItem>
                    <MenuItem onClick={handleImportDialogOpen}>
                        <FileUploadIcon sx={{ mr: 1 }} />
                        Import Todos
                    </MenuItem>
                </Menu>

                <Snackbar 
                    open={!!error} 
                    autoHideDuration={6000} 
                    onClose={() => setError(null)}
                    anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
                >
                    <Alert severity="error" onClose={() => setError(null)} sx={{ width: '100%' }}>
                        {error}
                    </Alert>
                </Snackbar>

                <Paper elevation={3} sx={{ p: 2 }}>
                    <Box component="form" onSubmit={addTodo} sx={{ marginBottom: 2 }}>
                        <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
                            <TextField
                                fullWidth
                                value={newTodo}
                                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setNewTodo(e.target.value)}
                                placeholder="Add a new todo"
                                variant="outlined"
                                size="small"
                            />
                            <FormControl size="small" sx={{ minWidth: 120 }}>
                                <InputLabel>Category</InputLabel>
                                <Select
                                    value={selectedCategory}
                                    onChange={handleCategoryChange}
                                    label="Category"
                                >
                                    {categories.map((category) => (
                                        <MenuItem key={category} value={category}>
                                            {category}
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                            <Button
                                type="submit"
                                variant="contained"
                                color="primary"
                            >
                                Add
                            </Button>
                        </Stack>
                    </Box>

                    <Box sx={{ mb: 2 }}>
                        <Typography variant="subtitle1" gutterBottom>
                            Filter by Category:
                        </Typography>
                        <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                            <Chip
                                label="All"
                                onClick={() => setFilterCategory('all')}
                                color={filterCategory === 'all' ? 'primary' : 'default'}
                                clickable
                            />
                            {categories.map((category) => (
                                <Chip
                                    key={category}
                                    label={category}
                                    onClick={() => setFilterCategory(category)}
                                    color={filterCategory === category ? 'primary' : 'default'}
                                    clickable
                                />
                            ))}
                        </Stack>
                    </Box>

                    <List>
                        {filteredTodos.map((todo) => (
                            <ListItem 
                                key={todo.id} 
                                dense
                                sx={{
                                    bgcolor: 'background.paper',
                                    mb: 1,
                                    borderRadius: 1,
                                    border: '1px solid',
                                    borderColor: 'divider'
                                }}
                            >
                                <Checkbox
                                    edge="start"
                                    checked={todo.isCompleted}
                                    onChange={() => toggleTodo(todo)}
                                />
                                <ListItemText
                                    primary={todo.title}
                                    secondary={todo.category}
                                    sx={{
                                        textDecoration: todo.isCompleted ? 'line-through' : 'none'
                                    }}
                                />
                                <ListItemSecondaryAction>
                                    <IconButton
                                        edge="end"
                                        onClick={() => openEditDialog(todo)}
                                        sx={{ mr: 1 }}
                                    >
                                        <EditIcon />
                                    </IconButton>
                                    <IconButton
                                        edge="end"
                                        onClick={() => deleteTodo(todo.id)}
                                    >
                                        <DeleteIcon />
                                    </IconButton>
                                </ListItemSecondaryAction>
                            </ListItem>
                        ))}
                    </List>
                </Paper>

                {/* Import Dialog */}
                <Dialog open={importDialogOpen} onClose={handleImportDialogClose}>
                    <DialogTitle>Import Todos</DialogTitle>
                    <DialogContent>
                        <Stack spacing={2} sx={{ mt: 1, minWidth: 300 }}>
                            <Typography variant="body2" color="textSecondary">
                                Paste your JSON or CSV data below:
                            </Typography>
                            <TextField
                                fullWidth
                                multiline
                                rows={4}
                                value={importData}
                                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setImportData(e.target.value)}
                                variant="outlined"
                                placeholder="Paste your data here..."
                            />
                        </Stack>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleImportDialogClose}>Cancel</Button>
                        <Button 
                            onClick={handleImport}
                            variant="contained"
                            color="primary"
                            disabled={!importData.trim()}
                        >
                            Import
                        </Button>
                    </DialogActions>
                </Dialog>

                {/* Edit Dialog */}
                <Dialog open={editDialogOpen} onClose={closeEditDialog}>
                    <DialogTitle>Edit Todo</DialogTitle>
                    <DialogContent>
                        <Stack spacing={2} sx={{ mt: 1, minWidth: 300 }}>
                            <TextField
                                fullWidth
                                label="Title"
                                value={editTitle}
                                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEditTitle(e.target.value)}
                                variant="outlined"
                            />
                            <FormControl fullWidth>
                                <InputLabel>Category</InputLabel>
                                <Select
                                    value={editCategory}
                                    onChange={(e: SelectChangeEvent) => setEditCategory(e.target.value)}
                                    label="Category"
                                >
                                    {categories.map((category) => (
                                        <MenuItem key={category} value={category}>
                                            {category}
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                        </Stack>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={closeEditDialog}>Cancel</Button>
                        <Button onClick={handleEditSubmit} variant="contained" color="primary">
                            Save
                        </Button>
                    </DialogActions>
                </Dialog>
            </Box>
        </Container>
    );
};
