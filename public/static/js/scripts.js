function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
csrftoken = Cookies('csrftoken');

var GameJS = function () {
    return {
        init: function () {
            GameJS.new_game('GET');
            jQuery('.new_game').click(function() {
                GameJS.new_game('POST');
            });
        },
        new_game: function(method) {
            jQuery.ajax({
                url: '/get_game/',
                method: method,
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (data) {
                    jQuery(".word_show").html(data.word_show);
                }
            })
        },
        check_word: function() {
            var word_chosen = 'A';
            jQuery.ajax({
                url: '/check_word/',
                method: 'POST',
                data: {'word': word_chosen},
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (data) {
                    alert(data);
                    console.log(JSON.stringify(data));
                }
            });
        },
    };
}();
