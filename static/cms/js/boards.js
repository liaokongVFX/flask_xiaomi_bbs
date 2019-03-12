// 添加版块
$(function () {
    $("#add-board-btn").click(function (event) {
        event.preventDefault();

        xtalert.alertOneInput({
            "text": "请输入版块名称",
            "placeholder": "版块名称",
            "confirmCallback": function (inputValue) {
                xtajax.post({
                    "url": "/cms/aboard/",
                    "data": {
                        "name": inputValue,
                    },
                    "success": function (data) {
                        if (data["code"] == 200) {
                            window.location.reload();
                        } else {
                            xtalert.alertInfo(data["message"]);
                        }
                    }
                });
            }
        });

    });
});

// 编辑版块
$(function () {
    $(".edit-board-btn").click(function (event) {
        event.preventDefault();

        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var board_id = tr.attr("data-id");

        xtalert.alertOneInput({
            "text": "请输入新的版块名称",
            "placeholder": name,
            "confirmCallback": function (inputValue) {
                xtajax.post({
                    "url": "/cms/uboard/",
                    "data": {
                        "board_id": board_id,
                        "name": inputValue,
                    },
                    "success": function (data) {
                        if (data["code"] == 200) {
                            window.location.reload();
                        } else {
                            xtalert.alertInfo(data["message"]);
                        }

                    }
                });
            }
        });
    });

});

// 删除版块
$(function () {
    $(".delete-board-btn").click(function (event) {
        event.preventDefault();

        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr("data-id");

        xtalert.alertConfirm({
            "msg": "您确定要删除这个版块吗？",
            "confirmCallback": function () {
                xtajax.post({
                    "url": "/cms/dboard/",
                    "data": {
                        "board_id": board_id
                    },
                    "success": function (data) {
                        if (data["code"] == 200) {
                            window.location.reload();
                        } else {
                            xtalert.alertInfo(data["message"]);
                        }
                    }
                });
            }
        });

    });
});
