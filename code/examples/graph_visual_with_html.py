import networkx as nx
from pyvis.network import Network
import random
import os

# 保持原有的生成代码不变
G = nx.read_graphml(r"C:\Users\86186\Desktop\法小询v2.0\code\民法\graph_chunk_entity_relation.graphml")
net = Network(height="100vh", notebook=True)
net.from_nx(G)

import random

for node in net.nodes:
    while True:
        # 随机生成一个颜色值
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        # 将生成的颜色从十六进制转换为 RGB 格式
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        # 检查是否接近红色（可以根据需要调整阈值）
        if not (r > 200 and g < 50 and b < 50):  # 调整阈值以避免接近红色的颜色
            break
    
    node["color"] = color

# 生成基础HTML
net.show("knowledge_graph.html")

# 读取生成的HTML并添加查询功能
with open("knowledge_graph.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 调整主视图位置
html_content = html_content.replace(
    '<div id="mynetwork"></div>',
    '<div id="mynetwork" style="margin-left: 300px; height: 100vh;"></div>'
)

# 添加查询面板
sidebar_html = '''
<div id="sidebar" style="position: fixed; left: 0; top: 0; width: 300px; height: 100vh; 
      background: white; padding: 20px; box-shadow: 2px 0 5px rgba(0,0,0,0.1); 
      overflow-y: auto; z-index: 1000;">
    <h2>知识图谱查询</h2>
    <input type="text" id="searchInput" placeholder="输入节点名称" 
           style="width: 100%; padding: 8px; margin-bottom: 10px;">
    <div id="resultInfo" style="margin-top: 20px; word-wrap: break-word;"></div>

    <!-- 添加询问窗口 -->
    <h2>询问窗口</h2>
    <input type="text" id="askInput" placeholder="输入问题" 
           style="width: 100%; padding: 8px; margin-bottom: 10px;">
    <button onclick="askQuestion()" 
            style="width: 100%; padding: 10px; background: #2196F3; color: white; 
                   border: none; cursor: pointer;">提问</button>
    <div id="askResult" style="margin-top: 20px; word-wrap: break-word;"></div>
</div>
'''

# 查询逻辑
js_code = '''
<script>
// 存储原始样式
let originalStyles = {
    nodes: new Map(),
    edges: new Map()
};

function storeOriginalStyles() {
    network.body.data.nodes.get().forEach(node => {
        originalStyles.nodes.set(node.id, {
            color: node.color,
            size: node.size
        });
    });
    network.body.data.edges.get().forEach(edge => {
        originalStyles.edges.set(edge.id, {
            color: edge.color,
            width: edge.width
        });
    });

    // 检查 originalStyles 是否正确填充
    console.log("Original Styles:", originalStyles);
}

function searchNode() {
    const searchTerm = document.getElementById('searchInput').value.trim().toLowerCase();
    if (!searchTerm) return;
    
    // 将输入的关键词按逗号分隔成数组
    const keywords = searchTerm.split(',').map(kw => kw.trim());
    
    const nodes = network.body.data.nodes.get();
    const edges = network.body.data.edges.get();
    let matchedNodes = new Set();
    
    // 重置所有样式
    nodes.forEach(node => {
        const original = originalStyles.nodes.get(node.id);
        node.color = original.color;
        node.size = original.size;
    });
    edges.forEach(edge => {
        const original = originalStyles.edges.get(edge.id);
        edge.color = original.color;
        edge.width = original.width;
    });

    // 查找匹配节点
    nodes.forEach(node => {
        keywords.forEach(keyword => {
            if (node.label && node.label.toLowerCase().includes(keyword)) {
                matchedNodes.add(node.id);
                node.color = '#FF8C00';
                node.size = 25;
            }
        });
    });

    // 高亮关联边
    edges.forEach(edge => {
        if ([edge.from, edge.to].some(id => matchedNodes.has(id))) {
            edge.color = '#FF8C00';
            edge.width = 3;
        }
    });

    // 更新网络
    network.body.data.nodes.update(nodes);
    network.body.data.edges.update(edges);
    
    // 显示结果信息
    const resultInfo = document.getElementById('resultInfo');
    resultInfo.innerHTML = `找到 ${matchedNodes.size} 个匹配节点<br>
                           找到 ${edges.filter(e => e.color === '#FF8C00').length} 条关联边`;

    // 如果有匹配节点，自动聚焦到第一个匹配节点
    const matchedNodesArray = Array.from(matchedNodes);
    if (matchedNodesArray.length > 0) {
        network.focus(matchedNodesArray[0], {scale: 0.8});
    }
}

// 初始化时存储原始样式
network.on("afterDrawing", function() {
    if (originalStyles.nodes.size === 0) {
        storeOriginalStyles();
    }
});
</script>
'''

# 添加询问逻辑
ask_js_code = '''
<script>
// 保持您的原始提取函数不变
function extractKeywordsFromResponse(responseText) {
    const lowLevelMatch = responseText.match(/\*\*低层次关键词\*\*:(.*?)(\\n|$)/);
    const highLevelMatch = responseText.match(/\*\*高层次关键词\*\*: (.*?)(\\n|$)/);

    const lowLevelKeywords = lowLevelMatch ? lowLevelMatch[1].split(", ").map(kw => kw.trim()) : [];
    const highLevelKeywords = highLevelMatch ? highLevelMatch[1].split(", ").map(kw => kw.trim()) : [];

    console.log("低层次关键词:", lowLevelKeywords);
    console.log("高层次关键词:", highLevelKeywords);

    return [...lowLevelKeywords, ...highLevelKeywords];
}

async function askQuestion() {
    try {
        const question = document.getElementById('askInput').value.trim();
        if (!question) return;

        const askResult = document.getElementById('askResult');
        askResult.innerHTML = "正在分析问题，请稍候...";

        // 清空之前的查询
        document.getElementById('searchInput').value = '';
        network.setSelection({nodes: [], edges: []});

        // 获取回答和关键词
        const response = await fetch('http://127.0.0.1:8020/query', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ query: question })
        });

        const data = await response.json();
        const answer = data.data || "无回答内容";
        const keywords = extractKeywordsFromResponse(answer);

        // 更新结果展示
        askResult.innerHTML = `<strong>回答：</strong><br>${answer}`;

        if (keywords.length > 0) {
            // 自动填充搜索框
            document.getElementById('searchInput').value = keywords.join(', ');
            
            // 执行高亮查询
            searchNode();
            
            // 延时启动路径追踪(等待1.5秒让高亮完成）
            setTimeout(() => {
                // 获取所有高亮节点（颜色为红色的节点）
                const highlightedNodes = network.body.data.nodes.get()
                    .filter(node => node.color === '#FF8C00')
                    .map(node => node.id);

                if (highlightedNodes.length >= 2) {
                    askResult.innerHTML += `<br><br><strong>发现${highlightedNodes.length}个相关节点，开始路径分析：</strong>`;
                    startAutoBFS(highlightedNodes);
                } else {
                    askResult.innerHTML += `<br><br>⚠️ 找到${highlightedNodes.length}个节点，至少需要2个节点进行路径分析`;
                }
            }, 1500);
        }

    } catch (error) {
        console.error("查询失败：", error);
        askResult.innerHTML = `<strong>错误：</strong>${error.message}`;
    }
}

// 自动路径追踪函数
function startAutoBFS(nodeIds) {
    // 使用前两个高亮节点
    const [startNode, endNode] = nodeIds.slice(0, 2);
    
    // BFS算法实现
    const visited = new Set([startNode]);
    const queue = [[startNode]];
    let foundPath = [];

    while (queue.length > 0) {
        const path = queue.shift();
        const currentNode = path[path.length-1];
        
        if (currentNode === endNode) {
            foundPath = path;
            break;
        }
        
        // 获取相邻节点
        const neighbors = network.body.nodes[currentNode].edges
            .map(edge => edge.fromId === currentNode ? edge.toId : edge.fromId)
            .filter(id => !visited.has(id));
        
        neighbors.forEach(neighbor => {
            visited.add(neighbor);
            queue.push([...path, neighbor]);
        });
    }

    // 可视化路径
    if (foundPath.length > 0) {
        visualizePath(foundPath);
    } else {
        document.getElementById('askResult').innerHTML += `<br>⛔ 未找到关联路径`;
    }
}

// 路径可视化函数
function visualizePath(path) {
    let step = 0;
    const pathAnimation = setInterval(() => {
        if (step < path.length) {
            // 高亮当前节点
            const node = network.body.data.nodes.get(path[step]);
            node.color = '#00FF00'; // 绿色表示路径
            node.size = 25;
            network.body.data.nodes.update(node);
            
            // 自动聚焦
            network.focus(path[step], {
                scale: 0.8 + (step * 0.05),
                animation: true
            });
            
            step++;
        } else {
            clearInterval(pathAnimation);
            // 显示路径说明
            const pathLabels = path.map(id => 
                network.body.data.nodes.get(id).label || id
            );
            document.getElementById('askResult').innerHTML += `
                <br><br>✅ 发现知识路径：
                <ol>${pathLabels.map(label => `<li>${label}</li>`).join('')}</ol>
            `;
        }
    }, 1200); // 1.2秒/步
}
</script>
'''
# 插入自定义HTML/JS
html_content = html_content.replace('</body>', f'{sidebar_html}{js_code}{ask_js_code}</body>')

# 保存修改后的文件
with open("knowledge_graph.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("生成完成！打开 knowledge_graph.html 进行交互式查询")