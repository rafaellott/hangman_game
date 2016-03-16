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
                url: '/new_game/',
                method: 'POST',
                data: {'new_game': '1'},
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (data) {
                    GameJS.check_word('GET');
                }
            })
        },
        check_word: function(letter) {
            if (letter == 'GET') {
                method = letter;
                letter = '';
            } else {
                method = 'POST';
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
                    if (parseInt(data.status) == 1) {
                        jQuery(".msg").removeClass('hidden alert-danger').addClass('alert-success');
                        jQuery(".typed_char").prop('disabled', true);
                    } else if (parseInt(data.status) == 0) {
                        jQuery(".msg").removeClass('hidden alert-success').addClass('alert-danger');
                        jQuery(".typed_char").prop('disabled', true);
                    } else {
                        jQuery(".msg").addClass('hidden');
                        jQuery(".typed_char").prop('disabled', false);
                    }
                    if (data.guessed_letter) {
                        var letters = data.guessed_letter;
                        html = "";
                        for (var i=0; i<letters.length; i++) {
                            html += "<span>" + letters[i] + "</span>";
                            console.info(letters[i]);
                        }
                        jQuery('.letters').html(html);
                    }
                    console.log(JSON.stringify(data));
                }
            });
        },
    };
}();
