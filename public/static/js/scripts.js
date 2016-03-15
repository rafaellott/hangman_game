function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
csrftoken = Cookies('csrftoken');

var GameJS = function () {
    return {
        init: function () {
            console.log("Starting game");
        },
        new_game: function(t) {

        },
        check_word: function() {
            var word_chosen = 'A';
            $.ajax({
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
