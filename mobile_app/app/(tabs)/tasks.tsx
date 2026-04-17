import { useState, useCallback } from 'react';
import { View, Text, TextInput, TouchableOpacity, FlatList, StyleSheet, KeyboardAvoidingView, Platform, ActivityIndicator, Alert } from 'react-native';
import { Stack, useFocusEffect } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import * as SecureStore from 'expo-secure-store';
import { apiClient } from '../../api/client';

export default function TasksScreen() {
    const [tasks, setTasks] = useState<any[]>([]);
    const [newTaskTitle, setNewTaskTitle] = useState('');
    const [loading, setLoading] = useState(true);
    const [userId, setUserId] = useState<string | null>(null);

    // 1. ЗАВАНТАЖЕННЯ ЗАДАЧ (GET)
    const fetchTasks = async () => {
        try {
            const uid = await SecureStore.getItemAsync('userId');
            setUserId(uid);
            if (!uid) return;

            // Стукаємо в твій роут: GET /tasks/my-tasks/{user_id}
            const res = await apiClient.get(`/tasks/my-tasks/${uid}`);
            
            if (Array.isArray(res.data)) {
                setTasks(res.data);
            } else if (res.data && Array.isArray(res.data.tasks)) {
                setTasks(res.data.tasks);
            }
        } catch (e: any) {
            console.error("Помилка завантаження задач:", e.response?.data || e.message);
        } finally {
            setLoading(false);
        }
    };

    // Оновлюємо список щоразу, коли користувач відкриває цю вкладку
    useFocusEffect(
        useCallback(() => {
            fetchTasks();
        }, [])
    );

    // 2. СТВОРЕННЯ ЗАДАЧІ (POST)
    const addTask = async () => {
        if (!newTaskTitle.trim() || !userId) return;
        
        try {
            // FastAPI чекає employer_id як query-параметр
            await apiClient.post(`/tasks/?employer_id=${userId}`, {
                title: newTaskTitle.trim(),
                description: "Створено з мобілки",
                price: 0 // Додай сюди поля, які вимагає твоя схема TaskCreate!
            });
            
            setNewTaskTitle('');
            fetchTasks();
        } catch (e: any) {
            console.error("Помилка створення задачі:", e.response?.data || e.message);
        }
    };

    // 3. ЗМІНА СТАТУСУ / ВЗЯТТЯ В РОБОТУ (PATCH)
    const takeTask = async (taskId: string) => {
        try {
            // FastAPI чекає freelancer_id як query-параметр
            await apiClient.patch(`/tasks/${taskId}/take?freelancer_id=${userId}`);
            fetchTasks();
        } catch (e: any) {
            console.error("Помилка взяття в роботу:", e.response?.data || e.message);
        }
    };

    // 4. ВИДАЛЕННЯ ЗАДАЧІ (DELETE) - Оскільки в тебе є proxy_delete
    const deleteTask = async (taskId: string) => {
        try {
            await apiClient.delete(`/tasks/${taskId}?employer_id=${userId}`);
            fetchTasks();
        } catch (e: any) {
            console.error("Помилка видалення задачі:", e.response?.data || e.message);
        }
    };
    
    // Дизайн однієї картки задачі
    const renderTask = ({ item }: { item: any }) => {
        // Логіка відображення статусу (підлаштуй під те, що реально повертає твій бекенд)
        const isCompleted = item.status === 'done' || item.status === 'completed';
        
        // Якщо status == 'todo', це коло пусте. Якщо 'in_progress' - можна зробити іншу іконку.
        // Поки що робимо класичний чекбокс.
        return (
            <View style={styles.taskCard}>
                {/* Кнопка зміни статусу */}
                <TouchableOpacity style={styles.checkboxContainer} onPress={() => takeTask(item.id || item._id)}>
                    <Ionicons 
                        name={isCompleted ? "checkmark-circle" : "ellipse-outline"} 
                        size={28} 
                        color={isCompleted ? "#075E54" : "#ccc"} 
                    />
                </TouchableOpacity>
                
                {/* Текст задачі */}
                <View style={styles.taskTextContainer}>
                    <Text style={[styles.taskTitle, isCompleted && styles.taskTitleCompleted]}>
                        {item.title}
                    </Text>
                    {item.status && <Text style={styles.taskStatusBadge}>{item.status}</Text>}
                </View>

                {/* Кнопка видалення */}
                <TouchableOpacity style={styles.deleteBtn} onPress={() => deleteTask(item.id || item._id)}>
                    <Ionicons name="trash-outline" size={24} color="#ff4444" />
                </TouchableOpacity>
            </View>
        );
    };

    return (
        <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === "ios" ? "padding" : undefined}>
            <Stack.Screen options={{ title: 'Мої задачі', headerStyle: { backgroundColor: '#075E54' }, headerTintColor: '#fff' }} />

            <View style={styles.inputSection}>
                <TextInput 
                    style={styles.input} 
                    placeholder="Що потрібно зробити?" 
                    value={newTaskTitle}
                    onChangeText={setNewTaskTitle}
                    onSubmitEditing={addTask}
                />
                <TouchableOpacity style={styles.addButton} onPress={addTask}>
                    <Ionicons name="add" size={24} color="#fff" />
                </TouchableOpacity>
            </View>

            {loading ? (
                <View style={styles.center}><ActivityIndicator size="large" color="#075E54" /></View>
            ) : (
                <FlatList
                    data={tasks}
                    keyExtractor={(item, index) => item.id?.toString() || item._id?.toString() || index.toString()}
                    renderItem={renderTask}
                    contentContainerStyle={styles.listContent}
                    ListEmptyComponent={<Text style={styles.emptyText}>Усі задачі виконані! 🎉</Text>}
                />
            )}
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f5f5f5' },
    center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
    inputSection: { flexDirection: 'row', padding: 15, backgroundColor: '#fff', elevation: 2, alignItems: 'center' },
    input: { flex: 1, backgroundColor: '#f0f0f0', paddingHorizontal: 15, paddingVertical: 10, borderRadius: 20, fontSize: 16, marginRight: 10 },
    addButton: { backgroundColor: '#075E54', width: 44, height: 44, borderRadius: 22, justifyContent: 'center', alignItems: 'center' },
    listContent: { padding: 15, paddingBottom: 100 },
    taskCard: { flexDirection: 'row', backgroundColor: '#fff', padding: 15, borderRadius: 12, marginBottom: 10, alignItems: 'center', elevation: 1 },
    checkboxContainer: { marginRight: 10 },
    taskTextContainer: { flex: 1 },
    taskTitle: { fontSize: 16, color: '#333' },
    taskTitleCompleted: { color: '#888', textDecorationLine: 'line-through' },
    taskStatusBadge: { fontSize: 10, color: '#888', marginTop: 4, textTransform: 'uppercase', fontWeight: 'bold' },
    deleteBtn: { paddingLeft: 10 },
    emptyText: { textAlign: 'center', marginTop: 50, fontSize: 16, color: '#888' }
});