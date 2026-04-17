// mobile_app/app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons'; // Вбудована бібліотека іконок

export default function TabLayout() {
    return (
        <Tabs
            screenOptions={{
                tabBarActiveTintColor: '#075E54', // Фірмовий темно-зелений колір активної вкладки
                tabBarInactiveTintColor: '#888', // Колір неактивної вкладки
                headerStyle: { backgroundColor: '#075E54' }, // Колір верхньої шапки
                headerTintColor: '#fff', // Колір тексту в шапці
                tabBarStyle: { height: 60, paddingBottom: 5 }, // Трохи збільшуємо меню
            }}
        >
            <Tabs.Screen
                name="chats"
                options={{
                    title: 'Чати',
                    tabBarIcon: ({ color }) => <Ionicons name="chatbubbles" size={28} color={color} />,
                }}
            />
            <Tabs.Screen
                name="tasks"
                options={{
                    title: 'Задачі',
                    tabBarIcon: ({ color }) => <Ionicons name="list" size={28} color={color} />,
                }}
            />
            <Tabs.Screen
                name="profile"
                options={{
                    title: 'Профіль',
                    tabBarIcon: ({ color }) => <Ionicons name="person" size={28} color={color} />,
                }}
            />
        </Tabs>
    );
}