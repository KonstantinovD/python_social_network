//Это основной код, который будет загружать букмарклет. Он отслеживает, была ли загружена jQuery на текущем сайте,
// и, если не была, загружает ее. Если библиотека уже была подключена, код выполняет функцию bookmarklet().
// - jquery_version – необходимая версия jQuery;
// - site_url и static_url – URL’ы нашего сайта и статических файлов;
// - min_width и min_height – минимальные ширина и высота в пикселях для картинок, которые будет загружать букмарклет.
(function(){
    var jquery_version = '3.3.1';
    var site_url = 'https://4bd3c7c83c3d.ngrok.io/';
    var static_url = site_url + 'static/';
    var min_width = 100;
    var min_height = 100;

    //В этом коде мы выполняем следующие действия:
    // - загружаем стили bookmarklet.css, добавляя случайное число для предотвращения кеширования стилей браузером;
    // - добавляем HTML-элемент в <body> текущего сайта. Элемент содержит <div> с изображениями, найденными на сайте;
    // - добавляем событие, которое удаляет наш HTML из документа сайта, когда пользователь кликает на кнопку закрытия
    // блока. Используем селектор #bookmarklet#close, чтобы найти элемент с ID close, у которого есть родительский
    // элемент с ID bookmarklet.
    // Селекторы jQuery позволяют нам находить HTML-элементы. Они возвращают все подходящие
    // объекты. Более подробную информацию о селекторах jQuery можно найти на странице
    // https://api.jquery.com/category/selectors/.
    function bookmarklet(msg) {
        // Загрузка CSS-стилей.
        var css = jQuery('<link>');
        css.attr({
            rel: 'stylesheet',
            type: 'text/css',
            href: static_url + 'css/bookmarklet.css?r=' +
                Math.floor(Math.random()*99999999999999999999)
        });
        jQuery('head').append(css);

        // Загрузка HTML.
        box_html = '<div id="bookmarklet"><a href="#"id="close">&times;</a>' +
            '<h1>Select an image to bookmark:</h1><divclass="images"></div></div>';
        jQuery('body').append(box_html);

        // Добавление скрытия букмарклета при нажатии на крестик.
        jQuery('#bookmarklet #close').click(function(){
            jQuery('#bookmarklet').remove();
        });

        // Находим картинки на текущем сайте и вставляем их в окно букмарклета.
        jQuery.each(jQuery('img[src$="jpg"]'), function(index, image) {
            if (jQuery(image).width() >= min_width && jQuery(image).height() >= min_height){
                image_url = jQuery(image).attr('src');
                jQuery('#bookmarklet .images').append(
                    '<a href="#"><img src="'+image_url +'" /></a>'
                );
            }
        });

        // Когда изображение выбрано, добавляем его в список сохраненных картинок на нашем сайте.
        jQuery('#bookmarklet .images a').click(function(e){
            selected_image = jQuery(this).children('img').attr('src');
            // Скрываем букмарклет.
            jQuery('#bookmarklet').hide();
            // Открываем новое окно с формой сохранения изображения.
            window.open(site_url +'images/create/?url=' + encodeURIComponent(selected_image)
                + '&title=' + encodeURIComponent(jQuery('title').text()), '_blank');
        });
    };

    // Проверка, подключена ли jQuery.
    if(typeof window.jQuery != 'undefined') {
        bookmarklet();
    } else {
        // Проверка, что атрибут $ окна не занят другим объектом.
        var conflict = typeof window.$ != 'undefined';
        // Создание тега <script> с загрузкой jQuery.
        var script = document.createElement('script');
        script.src = '//ajax.googleapis.com/ajax/libs/jquery/' + jquery_version + '/jquery.min.js';
        // Добавление тега в блок <head> документа.
        document.head.appendChild(script);
        // Добавление возможности использовать несколько попыток для загрузки jQuery.
        var attempts = 15;
        (function(){
            // Проверка, подключена ли jQuery
            if(typeof window.jQuery == 'undefined') {
                if(--attempts> 0) {
                    // Если не подключена, пытаемся снова загрузить
                    window.setTimeout(arguments.callee, 250)
                } else {
                    // Превышено число попыток загрузки jQuery, выводим сообщение.
                    alert('An error occurred while loading jQuery')
                }
            } else {
                bookmarklet();
            }
        })();
    }
})();