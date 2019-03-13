$(function () {
    var ue = UE.getEditor("editor", {
        "serverUrl": "/ueditor/upload/",
    });

    $("#submit-btn").click(function (event) {
        event.preventDefault();

        var titleInput = $("input[name='title']");
        var boardSelect = $("select[name='board-id']");

        var title = titleInput.val();
        var board_id = boardSelect.val();
        var content = ue.getContent();

        xtajax.post({
            "url": "/apost/",
            "data": {
                "title": title,
                "content": content,
                "board_id": board_id
            },
            "success": function (data) {
                if (data["code"] == 200) {
                    xtalert.alertConfirm({
                        "msg": "恭喜！帖子发表成功！",
                        "cancelText": "回到首页",
                        "confirmText": "再发一篇",
                        "cancelCallback": function () {
                            window.location = "/";
                        },
                        "confirmCallback":function () {
                            // titleInput.val("");
                            // ue.setContent("");
                            window.location.reload();
                        }
                    });
                }else {
                    xtalert.alertInfo(data["message"]);
                }

            }
        });
    });


});