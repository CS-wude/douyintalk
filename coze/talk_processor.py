# talk_processor - 抖音用户话术数据处理工具
# 将unique_id+nickname和话术数据转化为标准格式

async def main(args: Args) -> Output:
    """
    话术数据处理主函数
    输入: input1(unique_id+nickname) 和 input2(话术)
    输出: output(标准化的话术数据数组)
    """
    
    try:
        params = args.params
        
        # 获取输入参数
        unique_id_nickname = params.get('input1', "")
        talk_content = params.get('input2', "")
        
        # 确保输入为字符串类型
        unique_id_nickname_str = str(unique_id_nickname) if unique_id_nickname is not None else ""
        talk_content_str = str(talk_content) if talk_content is not None else ""
        
        # 构建输出数据对象
        data_item = {
            "fields": {
                "unique_id+nickname": unique_id_nickname_str,
                "话术": talk_content_str
            }
        }
        
        # 构建最终输出 - Array<Object>格式
        ret: Output = {
            "output": [data_item]
        }
        
    except Exception as e:
        # 错误处理：即使输入有问题也必须输出结果
        # 使用默认值生成输出
        default_data_item = {
            "fields": {
                "unique_id+nickname": "",
                "话术": ""
            }
        }
        
        ret: Output = {
            "output": [default_data_item]
        }
    
    return ret


# 如果需要处理多个用户数据的版本
async def main_batch(args: Args) -> Output:
    """
    批量话术数据处理主函数
    输入: input1(多个unique_id+nickname，逗号分隔) 和 input2(多个话术，逗号分隔)
    输出: output(标准化的话术数据数组)
    """
    
    try:
        params = args.params
        
        # 获取输入参数
        unique_id_nicknames = params.get('input1', "")
        talk_contents = params.get('input2', "")
        
        # 确保输入为字符串类型
        unique_id_nicknames_str = str(unique_id_nicknames) if unique_id_nicknames is not None else ""
        talk_contents_str = str(talk_contents) if talk_contents is not None else ""
        
        # 分割输入数据（如果有多个的话）
        unique_id_list = [item.strip() for item in unique_id_nicknames_str.split(',') if item.strip()]
        talk_list = [item.strip() for item in talk_contents_str.split(',') if item.strip()]
        
        # 如果输入为空，创建默认项
        if not unique_id_list and not talk_list:
            unique_id_list = [""]
            talk_list = [""]
        
        # 确保两个列表长度一致，以较短的为准
        min_length = max(1, min(len(unique_id_list), len(talk_list)) if unique_id_list and talk_list else 1)
        
        # 生成输出数据
        output_data = []
        
        for i in range(min_length):
            unique_id_nickname = unique_id_list[i] if i < len(unique_id_list) else ""
            talk_content = talk_list[i] if i < len(talk_list) else ""
            
            data_item = {
                "fields": {
                    "unique_id+nickname": unique_id_nickname,
                    "话术": talk_content
                }
            }
            
            output_data.append(data_item)
        
        # 构建最终输出
        ret: Output = {
            "output": output_data
        }
        
    except Exception as e:
        # 错误处理：使用默认值生成输出
        default_data_item = {
            "fields": {
                "unique_id+nickname": "",
                "话术": ""
            }
        }
        
        ret: Output = {
            "output": [default_data_item]
        }
    
    return ret


