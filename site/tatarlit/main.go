package main

import (
	"fmt"
	"net/http"
)

func main() {
	fs := http.FileServer(http.Dir("./"))
	// Обрабатываем HTTP запросы
	http.Handle("/", fs)
	// Указываем порт, на котором будет запущен сервер
	port := ":8080"
	fmt.Println("Запуск сервера на порту", port, "\n", "http://localhost:8080/")
	// Запускаем сервер
	http.ListenAndServe(port, nil)
}
