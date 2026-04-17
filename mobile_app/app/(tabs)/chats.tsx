import { useState, useEffect, useCallback } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, ActivityIndicator, RefreshControl } from 'react-native';
import { router, Stack, useFocusEffect } from 'expo-router';
import { apiClient } from '../../api/client';

export default function ChatsListScreen() {
    const [chatList, setChatList] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);

    // Функція, яка стукає в Парсер за списком кімнат
    const fetchChats = async () => {
        try {
            // ТУТ ВАЖЛИВО: підстав правильний ендпоінт твого бекенду!
            // Я припустив, що він називається /chat/rooms або /chat/list
            const res = await apiClient.get('/chat/rooms'); 
            
            // Якщо бекенд повертає масив
            if (Array.isArray(res.data)) {
                setChatList(res.data);
            }
        } catch (e: any) {
            console.error("Помилка завантаження списку чатів:", e.response?.data || e.message);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    // Завантажуємо дані при кожному поверненні на цю вкладку
    useFocusEffect(
        useCallback(() => {
            fetchChats();
        }, [])
    );

    const onRefresh = () => {
        setRefreshing(true);
        fetchChats();
    };

    const openChat = (roomId: string) => {
        router.push(`/chat/${roomId}`);
    };

    const renderChatItem = ({ item }: { item: any }) => {
        // Запобіжник, якщо бекенд віддав трохи інші поля
        const roomName = item.name || `Кімната #${item.id || item.room_id}`;
        const lastMsg = item.lastMessage || item.last_message || 'Немає повідомлень...';
        
        return (
            <TouchableOpacity style={styles.chatItem} onPress={() => openChat(item.id || item.room_id)}>
                <View style={styles.avatar}>
                    <Text style={styles.avatarText}>{roomName.charAt(0).toUpperCase()}</Text>
                </View>
                <View style={styles.chatInfo}>
                    <View style={styles.chatHeader}>
                        <Text style={styles.chatName}>{roomName}</Text>
                        {/* Якщо є час останнього повідомлення - виводимо */}
                        {item.time && <Text style={styles.chatTime}>{item.time}</Text>}
                    </View>
                    <Text style={styles.lastMessage} numberOfLines={1}>{lastMsg}</Text>
                </View>
            </TouchableOpacity>
        );
    };

    return (
        <View style={styles.container}>
            <Stack.Screen options={{ title: 'Мої повідомлення', headerStyle: { backgroundColor: '#075E54' }, headerTintColor: '#fff' }} />
            
            {loading ? (
                <View style={styles.center}>
                    <ActivityIndicator size="large" color="#075E54" />
                </View>
            ) : chatList.length === 0 ? (
                <View style={styles.center}>
                    <Text style={styles.emptyText}>У вас поки немає жодного чату 😿</Text>
                </View>
            ) : (
                <FlatList
                    data={chatList}
                    keyExtractor={(item, index) => item.id?.toString() || item.room_id?.toString() || index.toString()}
                    renderItem={renderChatItem}
                    ItemSeparatorComponent={() => <View style={styles.separator} />}
                    refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={['#075E54']} />}
                />
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#fff' },
    center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
    emptyText: { fontSize: 16, color: '#888' },
    chatItem: { flexDirection: 'row', padding: 15, alignItems: 'center' },
    avatar: { width: 50, height: 50, borderRadius: 25, backgroundColor: '#128C7E', justifyContent: 'center', alignItems: 'center', marginRight: 15 },
    avatarText: { color: '#fff', fontSize: 20, fontWeight: 'bold' },
    chatInfo: { flex: 1 },
    chatHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 5 },
    chatName: { fontSize: 16, fontWeight: 'bold', color: '#000' },
    chatTime: { fontSize: 12, color: '#888' },
    lastMessage: { fontSize: 14, color: '#555' },
    separator: { height: 1, backgroundColor: '#eee', marginLeft: 80 }
});