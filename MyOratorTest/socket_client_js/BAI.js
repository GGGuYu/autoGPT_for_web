function send_message(message)
{
// 获取输入框和按钮元素
const inputEl = document.querySelector('.n-input__textarea-el');
const submitBtn = document.querySelector('.n-button.n-button--primary-type.n-button--medium-type');

// 向输入框添加文本
inputEl.value = message;
// 清空提示词
inputEl.setAttribute('placeholder', '');
  // 删除按钮的禁用样式
submitBtn.classList.remove('n-button--disabled');
// 触发input事件
inputEl.dispatchEvent(new Event('input', { bubbles: true }));
setTimeout(function() {
  // 触发按钮点击事件
  submitBtn.click();
}, 50);
}


// 创建WebSocket对象
const socket = new WebSocket('ws://localhost:8888');

// 发送哥要python的消息方法
function sendMessage(message) {
  socket.send(message);
}

const targetNode = document.documentElement;
const config = { childList: true, subtree: true };

let old_content = "old";

const getTextContent = () => {
  // const elements = document.querySelectorAll('.overflow-hidden.text-sm.items-end, .overflow-hidden.text-sm.items-start');
  const elements = document.querySelectorAll('.overflow-hidden.text-sm.items-start');
  let content = '';
  // elements.forEach(element => {
  //   content += element.textContent;
  // });
  content = elements[elements.length-1].textContent;
  console.log(content);
  return content
};

// 初始获取一次内容
// getTextContent();

// 监听整个文档树的子节点变化
const observer = new MutationObserver(mutationsList => {
  for (let mutation of mutationsList) {
    if (mutation.type === 'childList') {  
      let timely_content = '';
      let cur_content = "null";
      cur_content = getTextContent();
      setTimeout(function() {
        timely_content = getTextContent();
        if(cur_content == timely_content && old_content != cur_content && cur_content.length >= 21)
        {
          sendMessage(cur_content.substring(18, cur_content.length));
          old_content = cur_content;
          console.log('应该是输出完毕了！')
        }
      }, 2200);
    }
  }
});

observer.observe(targetNode, config);
// 监听WebSocket连接打开事件
socket.addEventListener('open', function (event) {
  console.log('WebSocket连接已打开');
});

// 监听WebSocket接收消息事件
socket.addEventListener('message', function (event) {
  console.log('收到消息:', event.data);
  //发送给星期三
  send_message(event.data);
});

setTimeout(function() {
  sendMessage('连接开始！')
}, 3000);
