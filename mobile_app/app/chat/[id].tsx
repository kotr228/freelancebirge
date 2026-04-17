// mobile_app/app/chat/[id].tsx
import { useState, useEffect, useRef } from 'react';
import { View, Text, TextInput, TouchableOpacity, FlatList, StyleSheet, KeyboardAvoidingView, Platform } from 'react-native';
import { useLocalSearchParams, Stack } from 'expo-router';
import * as SecureStore from 'expo-secure-store';
import { apiClient } from '../../api/client';

export default function ChatRoomScreen() {
    // ДІСТАЄМО ID КІМНАТИ З URL (НАВІГАЦІЇ)
    const { id } = useLocalSearchParams();
    const roomId = id as string;

    const [messages, setMessages] = useState<any[]>([]);
    const [text, setText] = useState('');
    const [userId, setUserId] = useState<string | null>(null);
    const ws = useRef<WebSocket | null>(null);

    useEffect(() => {
        const initChat = async () => {
            // Дістаємо, хто ми є, з пам'яті телефону
            const storedUserId = await SecureStore.getItemAsync('userId');
            setUserId(storedUserId);

            if (!storedUserId) return;

            try {
                const res = await apiClient.get(`/chat/${roomId}/history`);
                if (Array.isArray(res.data)) {
                    setMessages(res.data);
                } else if (res.data && res.data.messages) {
                    setMessages(res.data.messages);
                }
            } catch (e) {
                console.error("Помилка завантаження історії:", e);
            }

            // Відкриваємо сокет з реальним ID кімнати та реальним юзером
            ws.current = new WebSocket(`ws://10.0.2.2:8002/chat/ws/${roomId}/${storedUserId}`);

            ws.current.onmessage = (event) => {
                const msgData = JSON.parse(event.data);
                if (msgData.type === 'new_message') {
                    setMessages(prev => [msgData.data, ...prev]);
                }
            };
        };

        initChat();

        return () => {
            ws.current?.close();
        };
    }, [roomId]);

    const sendMessage = async () => {
        if (!text.trim() || !userId) return;
        try {
            await apiClient.post(`/chat/${roomId}/send?user_id=${userId}`, { text: text });
            setText('');
        } catch (e) {
            console.error("Помилка відправки:", e);
        }
    };

    const renderMessage = ({ item }: { item: any }) => {
        const isMe = item.sender_id === userId;
        return (
            <View style={[styles.msgWrapper, isMe ? styles.msgWrapperMe : styles.msgWrapperOther]}>
                {!isMe && <Text style={styles.senderName}>{item.sender_id}</Text>}
                <View style={[styles.msgBubble, isMe ? styles.msgMe : styles.msgOther]}>
                    {/* ТУТ БУЛА ПОМИЛКА. Тепер просто styles.msgText */}
                    <Text style={styles.msgText}>{item.text}</Text> 
                </View>
            </View>
        );
    };

    if (!userId) return <View style={styles.container}><Text>Завантаження...</Text></View>;

    return (
        <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === "ios" ? "padding" : undefined}>
            {/* Динамічний заголовок сторінки */}
            <Stack.Screen options={{ title: `Кімната #${roomId}`, headerStyle: { backgroundColor: '#075E54' }, headerTintColor: '#fff' }} />

            <FlatList
                data={messages}
                keyExtractor={(item, index) => item.id || index.toString()}
                renderItem={renderMessage}
                inverted
                contentContainerStyle={styles.listContainer}
            />

            <View style={styles.inputContainer}>
                <TextInput style={styles.input} value={text} onChangeText={setText} placeholder="Напишіть повідомлення..." />
                <TouchableOpacity style={styles.sendButton} onPress={sendMessage}>
                    <Text style={styles.sendIcon}>➤</Text>
                </TouchableOpacity>
            </View>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#E5DDD5' },
    listContainer: { padding: 10 },
    msgWrapper: { marginBottom: 10, maxWidth: '80%' },
    msgWrapperMe: { alignSelf: 'flex-end' },
    msgWrapperOther: { alignSelf: 'flex-start' },
    senderName: { fontSize: 12, color: '#555', marginLeft: 5, marginBottom: 2 },
    msgBubble: { padding: 10, borderRadius: 15, elevation: 1 },
    msgMe: { backgroundColor: '#DCF8C6', borderBottomRightRadius: 0 },
    msgOther: { backgroundColor: '#FFF', borderBottomLeftRadius: 0 },
    msgText: { fontSize: 16, color: '#000' },
    inputContainer: { flexDirection: 'row', padding: 10, backgroundColor: '#fff', alignItems: 'center' },
    input: { flex: 1, backgroundColor: '#F0F0F0', padding: 12, borderRadius: 25, fontSize: 16, marginRight: 10 },
    sendButton: { backgroundColor: '#075E54', width: 46, height: 46, borderRadius: 23, justifyContent: 'center', alignItems: 'center' },
    sendIcon: { color: '#fff', fontSize: 20, marginLeft: 2 }
});