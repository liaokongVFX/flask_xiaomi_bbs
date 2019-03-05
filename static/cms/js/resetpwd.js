$(function () {
    $("#submit").click(function (event) {
        // 阻止按钮默认的提交表单事件
        event.preventDefault();

        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        xtajax.post({
            "url": "/cms/resetpwd/",
            "data": {
                "oldpwd": oldpwd,
                "newpwd": newpwd,
                "newpwd2": newpwd2
            },
            "success": function (data) {
                if(data['code'] == 200) {
                    xtalert.alertSuccessToast("密码修改成功！");
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
                } else {
                    var message = data["message"];
                    xtalert.alertInfo(message);
                }
            },
            "fail": function (error) {
                xtalert.alertNetworkError();
            }
        })
    });
});