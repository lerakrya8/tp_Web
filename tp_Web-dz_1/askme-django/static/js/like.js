$('.js-like').click(function (ev) {
    ev.preventDefault();
    let $this = $(this),
        qid = $this.data('qid');

    $.ajax('like', {
        method: 'POST',
        data: {
            qid: qid,
        }
    }).done(function (data) {
         $('#questions_likes-' + qid).text(data.questions_likes);
        console.log(data)
    })

    console.log('question id = ' + qid);
})

$('.js-answer-like').click(function (ev) {
    ev.preventDefault();
    let $this = $(this),
        qid = $this.data('qid');

    $.ajax('answer-like', {
        method: 'POST',
        data: {
            qid: qid,
        }
    }).done(function (data) {
         $('#answers_likes-' + qid).text(data.answers_likes);
        console.log(data)
    })

    console.log('answer id = ' + qid);
})