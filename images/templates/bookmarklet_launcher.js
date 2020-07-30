(function () {
    if(window.myBookmarklet !== undefined){
        myBookmarklet();
    }
    else{
        document.body.appendChild(
            document.createElement('script')
        ).src='https://4bd3c7c83c3d.ngrok.io/static/js/bookmarklet.js?r=' +
            Math.floor(Math.random()*99999999999999999999);
    }
})();
//Этот фрагмент проверяет, был ли уже загружен код букмарклета, который хранится в переменной myBookmarklet. Так мы
// избегаем лишней загрузки кода в случае, когда пользователь повторно кликает на букмарклет. Если переменная
// myBookmarklet не содержит значения, код загружает другой JavaScript-файл, добавляя <script>-элемент в документ.
// Тег <script> загружает bookmarklet.js, добавляя к названию случайное число. Это необходимо для предотвращения
// кеширования файла браузером.
// Актуальный код букмарклета будет находиться в файле bookmarklet.js. Это позволит обновлять выполняемый код без
// необходимости для пользователей обновлять закладку, которую они добавили ранее.