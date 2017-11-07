<script type="text/javascript">

    function $(id) { return document.getElementById(id); }

    // 在光标处插入字符串
    // myField    文本框对象
    // 要插入的值
    function insertAtCursor(myField, myValue) 
    {
        //IE support
        if (document.selection) 
        {
            myField.focus();
            sel            = document.selection.createRange();
            sel.text    = myValue;
            sel.select();
        }
        //MOZILLA/NETSCAPE support
        else if (myField.selectionStart || myField.selectionStart == '0') 
        {
            var startPos    = myField.selectionStart;
            var endPos        = myField.selectionEnd;
            // save scrollTop before insert
            var restoreTop    = myField.scrollTop;
            myField.value    = myField.value.substring(0, startPos) + myValue + myField.value.substring(endPos, myField.value.length);
            if (restoreTop > 0)
            {
                // restore previous scrollTop
                myField.scrollTop = restoreTop;
            }
            myField.focus();
            myField.selectionStart    = startPos + myValue.length;
            myField.selectionEnd    = startPos + myValue.length;
        } else {
            myField.value += myValue;
            myField.focus();
        }
    }
</script>