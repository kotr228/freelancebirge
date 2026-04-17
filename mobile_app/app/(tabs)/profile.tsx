import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { router } from 'expo-router';

export default function ProfileScreen() {
    const handleLogout = async () => {
        await SecureStore.deleteItemAsync('userToken');
        await SecureStore.deleteItemAsync('userId');
        router.replace('/'); // Повертаємось на екран логіну
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Профіль Котика 🐾</Text>
            <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
                <Text style={styles.logoutText}>Вийти з акаунта</Text>
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#f5f5f5' },
    title: { fontSize: 22, fontWeight: 'bold', marginBottom: 30, color: '#333' },
    logoutBtn: { backgroundColor: '#ff4444', padding: 15, borderRadius: 10 },
    logoutText: { color: '#fff', fontWeight: 'bold', fontSize: 16 }
});