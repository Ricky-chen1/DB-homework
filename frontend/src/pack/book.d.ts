// 定义单本书籍的数据结构
export interface Book {
    id: number;               // 书籍 ID
    publisher_id: number,
    title: string;            // 书籍标题
    author: string;           // 作者
    price: string;            // 价格，格式为字符串
    status: string;           // 状态，例如 "available"
    cover_url: string | null; // 封面图片链接，可能为 null
    created_at: string;       // 创建时间，格式为 ISO 时间字符串
    categories: string[];     // 书籍分类，字符串数组
  }
  
  // 定义获取书籍列表返回的结果结构
  export interface GetBookListResponse {
    code: number;             // 状态码，0 表示成功，其他值表示失败
    msg: string;              // 状态信息或错误信息
    data: Book[];             // 书籍数据数组
  }

  export interface GetBookDetailResponse{
    code: number;
    msg: string;
    data: Book;
  }
  