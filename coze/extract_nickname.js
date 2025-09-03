// 抖音用户信息提取器
// 输入: 包含多个用户信息的集成报告JSON字符串
// 输出: key0为所有用户的unique_id+nickname连接字符串，逗号分隔

async function main({ params }) {
    try {
        // 解析输入的JSON字符串
        const reportData = JSON.parse(params.input);
        
        let result = "未知用户";
        
        // 处理集成报告格式 - 包含results数组
        if (reportData.results && Array.isArray(reportData.results)) {
            const userStrings = [];
            
            // 遍历所有用户结果，提取unique_id和nickname
            reportData.results.forEach(userResult => {
                if (userResult.user_info) {
                    const userInfo = userResult.user_info;
                    const uniqueId = userInfo.unique_id || "";
                    const nickname = userInfo.nickname || "";
                    
                    // 将unique_id和nickname连接
                    const userString = uniqueId + nickname;
                    
                    if (userString) {
                        userStrings.push(userString);
                    }
                }
            });
            
            if (userStrings.length > 0) {
                result = userStrings.join(", "); // 多个用户用逗号分隔
            }
        }
        // 处理单个用户格式
        else if (reportData.user_info) {
            const userInfo = reportData.user_info;
            const uniqueId = userInfo.unique_id || "";
            const nickname = userInfo.nickname || "";
            
            result = uniqueId + nickname;
        }
        
        // 构建输出
        const ret = {
            "key0": result
        };

        return ret;
        
    } catch (error) {
        // JSON解析失败时的错误处理
        const ret = {
            "key0": "解析失败: " + error.message
        };
        
        return ret;
    }
}