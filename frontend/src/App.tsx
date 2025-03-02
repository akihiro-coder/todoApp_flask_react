// Reactの`useState`（状態管理）と`useEffect`（副作用処理）をインポート
import { useState, useEffect } from "react";
// FlaskのAPIと通信するため
import axios from "axios";



// ToDoの型
type ToDo = {
    id: number;
    title: string;
    completed: boolean;
};


const App = () => {
    // ToDoリストを管理する`useState`
    const [todos, setTodos] = useState<Todo[]>([]);

    // 新しいToDOの入力値を管理する`useState`
    const [newTodo, setNewTodo] = useState("");

    // ToDoの一覧を取得(FlaskのAPIと通信)
    const fetchTodos = async () => {
        try {
            // Flaskの`Get /todos`エンドポイントにリクエストを送信
            const response = await axios.get("http://127.0.0.1:5000/todos");

            // 取得したToDoリストを`todos`ステートに保存
            setTodos(response.data);
        } catch (error) {
            console.error("Error fetching todos:", error);
        }
    }
};
