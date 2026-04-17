// mobile_app/app/index.tsx
import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { router } from 'expo-router';
import { jwtDecode } from "jwt-decode";
import { apiClient } from '../api/client';

export default function LoginScreen() {
    // Дані вже тут, щоб не друкувати на віртуальній клавіатурі :)
    const [username, setUsername] = useState('jolie_cat'); 
    const [password, setPassword] = useState('super_secret_123');
    const [loading, setLoading] = useState(false);

    const handleLogin = async () => {
        setLoading(true);
        try {
            // 1. Стукаємо в Парсер
            const response = await apiClient.post('/auth/login', {
                username,
                password
            });

            const token = response.data.access_token;

            // ЯК МАЄ БУТИ (Правильно):
            await SecureStore.setItemAsync('userToken', token);

            // Розпаковуємо токен і дістаємо справжній UUID
            const decodedToken = jwtDecode(token);

            if (decodedToken.sub) {
                await SecureStore.setItemAsync('userId', decodedToken.sub);
            } else {
            Alert.alert("Помилка", "Некоректний токен: відсутній ID користувача");
            return; // Зупиняємо логін
            }
            
            Alert.alert('Успіх!', 'Котик залогінився 🐾');
            router.replace('/(tabs)/chats')

            // 3. Переходимо на наступний екран
            router.replace('/(tabs)/chats')

        } catch (error) {
            console.error('Помилка логіну:', error);
            Alert.alert('Помилка', 'Неправильний логін або пароль чи сервер недоступний');
        } finally {
            setLoading(false);
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Freelance Birge</Text>
            <Text style={styles.subtitle}>Вхід у систему</Text>

            <TextInput
                style={styles.input}
                placeholder="Юзернейм"
                value={username}
                onChangeText={setUsername}
                autoCapitalize="none"
            />

            <TextInput
                style={styles.input}
                placeholder="Пароль"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
            />

            <TouchableOpacity style={styles.button} onPress={handleLogin} disabled={loading}>
                <Text style={styles.buttonText}>{loading ? 'Вхід...' : 'Увійти'}</Text>
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: 'center', padding: 20, backgroundColor: '#f5f5f5' },
    title: { fontSize: 32, fontWeight: 'bold', textAlign: 'center', marginBottom: 10, color: '#333' },
    subtitle: { fontSize: 18, textAlign: 'center', marginBottom: 30, color: '#666' },
    input: { backgroundColor: '#fff', padding: 15, borderRadius: 10, marginBottom: 15, borderWidth: 1, borderColor: '#ddd' },
    button: { backgroundColor: '#007bff', padding: 15, borderRadius: 10, alignItems: 'center' },
    buttonText: { color: '#fff', fontSize: 18, fontWeight: 'bold' }
});