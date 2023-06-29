//发送信息给bing的函数
const addTextToTextArea = (message) => {
  const textAreaElement = findTextAreaElement(document.body);
  if (textAreaElement) {
    // 向<textarea>元素添加文本
    textAreaElement.value = message;

    // 设置data-input和data-suggestion属性的值
    const labelElement = textAreaElement.closest('.text-input');
    if (labelElement) {
      labelElement.dataset.input = message;
      labelElement.dataset.suggestion = message;
    }
    // 聚焦<textarea>元素并设置为输入状态
    textAreaElement.focus();
    textAreaElement.select();
    textAreaElement.dispatchEvent(new Event('input', { bubbles: true }));
    // 模拟用户按下"Enter"键
    const enterKeyEvent = new KeyboardEvent('keydown', { key: 'Enter' });
    setTimeout(function() {
      textAreaElement.dispatchEvent(enterKeyEvent);
    }, 300);
  }
};

const findTextAreaElement = (element) => {
  if (element.tagName === 'TEXTAREA') {
    return element;
  }

  // 递归遍历子节点
  var children = element.children;
  for (var i = 0; i < children.length; i++) {
    const childResult = findTextAreaElement(children[i]);
    if (childResult) {
      return childResult;
    }
  }

  // 如果当前元素有 shadowRoot，则遍历其子节点
  if (element.shadowRoot) {
    var shadowChildren = element.shadowRoot.children;
    for (var j = 0; j < shadowChildren.length; j++) {
      const shadowResult = findTextAreaElement(shadowChildren[j]);
      if (shadowResult) {
        return shadowResult;
      }
    }
  }

  return null;
};

//---------------------------------------------------------以上是发送信息的函数

var messageQueue = [];//机器人的所有信息
const getTextContent = (element) => {
  if (element.className === 'ac-textBlock') {
    messageQueue.push(element.textContent);//只要是机器人的信息就装入队列
    // console.log(element.textContent);
  }
  // 递归遍历子节点
  var children = element.children;
  for (var i = 0; i < children.length; i++) {
    getTextContent(children[i]);
  }

  // 如果当前元素有 shadowRoot，则遍历其子节点
  if (element.shadowRoot) {
    var shadowChildren = element.shadowRoot.children;
    for (var j = 0; j < shadowChildren.length; j++) {
      getTextContent(shadowChildren[j]);
    }
  }
};
//检查信息函数，调一次返回一次当前页面最后一个回复信息
function checkOneceMessage(root)
{
  // 获取一次内容
  getTextContent(root);
  let Popmessage = String(messageQueue.pop());//取出机器人的最新消息
  // console.log(Popmessage);
  messageQueue = [];//置空队列下次使用
  //如果机器人没有信息，就返回null,方便做判断
  if(Popmessage == null || Popmessage.length == 0 || Popmessage == 'undefined' || Popmessage == 'null')
  {
    return null;
  }
  return Popmessage;
}

//---------------------------------------------------------以上是获取信息的函数

// 创建WebSocket对象
const socket = new WebSocket('ws://localhost:8888');
// 封装一下socket发送python的消息方法
function sendMessage(message) {
  socket.send(message);
}
// 监听WebSocket连接打开事件
socket.addEventListener('open', function (event) {
  console.log('WebSocket连接已打开');
});
// 监听WebSocket接收消息事件
socket.addEventListener('message', function (event) {
  console.log('收到消息:', event.data);
  //发送给机器人
  addTextToTextArea(event.data);
});

//---------------------------------------------------------以上是服务器相关函数与对象


//------------------------主程序 通过定时器监控网页实现模拟人们发送信息看到信息
var old_message = '';
var cur_message = '';
var locked = false;
// 这个标志表示刚刚才发送过消息，那么至少应该等一次检测之后才有可能发送消息，而不要出现因为卡顿导致快速发了两条消息的情况。
var sign = false; 
var net_bug_cnt = 0;//可以忽略掉的对比次数,因为如果刚刚发了，短时间内的变化说明是网络情况不稳定
var net_bug_cnt_max = 5;//最大上限,通过调整这个数可以翻倍等待时间
//先发送一个消息告诉服务器，已经连接开始了
setTimeout(function() {
  sendMessage('连接开始！')
}, 2000);

//设置定时器,每过一段时间调用一次checkOneceMessage函数检查信息，并把返回信息赋值给cur_message然后打印
setInterval(function(){
  cur_message = checkOneceMessage(document.body);
  if(cur_message == null)
  {
    cur_message = old_message;
  }
  //如果刚刚才发送过消息，那么这一次定时检测可以不做，因为连续两次发送消息肯定说明网络卡了
  //此时应该让old和cur相等然后直接退出
  if(sign)
  {
    old_message = cur_message; //此时如果发生了变化是因为网络问题，所以忽略掉本次网络卡顿
    net_bug_cnt++;
    if(net_bug_cnt >= net_bug_cnt_max)
    {
      net_bug_cnt = 0;
      sign = false;
    }
    return;
  }
  //不等的话说明正在变化，不需要发送
  if(cur_message != old_message)
  {
    old_message = cur_message;
    //如果不等，说明是在变化，因此此时锁打开，等到这次变化结束后相等时，就可以发送
    locked = true;//打开回复锁，说明机器人正在回复
  }else{
    //相等的时候有可能是没操作，也有可能是输出完毕，通过locked回复锁来区分
    if(locked)
    {
      cur_message = cur_message.trim();//去除两端多余空格
      let last_char = cur_message[cur_message.length-1];
      console.log("cur_message: "+cur_message);
      console.log("last_char: "+last_char);
      //减少输出卡了之后出现的回复一半的问题，至少回复是个整句，这样出错的概率大大减小，也可以调快定时器频率
      if (['。', '.', '?', '!', '？', '！','>','�','�'].includes(last_char))
      {
        sendMessage(cur_message);
        console.log("发送给用户的信息:" + cur_message);
        //发送了之后将锁归位，表示进入了静默
        sign = true;//说明刚刚发过了的标志位
        locked = false;
      }
    }
  }
}
  ,1200);
