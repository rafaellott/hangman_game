function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
csrftoken = Cookies('csrftoken');

var GameJS = function () {
    return {
        init: function () {
            GameJS.check_word('GET');
            jQuery('.new_game').click(function() {
                GameJS.new_game();
            });

            jQuery('.typed_char').keyup(function() {
                var letter = jQuery(this).val().toUpperCase();
                jQuery(this).val('');
                GameJS.check_word(letter);
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
        check_word: function(letter) {
            if (letter == 'POST') {
                method = letter;
                letter = '';
            } else {
                method = 'GET'
            }
            jQuery.ajax({
                url: '/check_word/',
                method: method,
                data: {'letter': letter},
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (data) {
                    jQuery(".word_show").html(data.word_show);
                    if (parseInt(data.remaining) == 0) {
                        jQuery(".remaining").parent().remove();
                    } else {
                        jQuery(".remaining").html(data.remaining);
                    }
                    jQuery(".msg").html(data.msg);
                    console.log(JSON.stringify(data));
                }
            });
        },
    };
}();
