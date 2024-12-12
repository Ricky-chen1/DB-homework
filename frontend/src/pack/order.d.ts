// 定义单个订单的数据结构
export interface Order {
    id: number;             // 订单 ID
    buyer_id: number;       // 买家 ID
    seller_id: number;      // 卖家 ID
    book_id: number;        // 书籍 ID
    price: string;          // 价格，格式为字符串
    status: string;         // 订单状态，例如 "pending"
    created_at: string;     // 创建时间，格式为 ISO 时间字符串
    updated_at: string;     // 更新时间，格式为 ISO 时间字符串
  }
  
  // 定义获取订单列表返回的结果结构
  export interface GetOrderListResponse {
    code: number;           // 状态码，0 表示成功，其他值表示失败
    msg: string;            // 状态信息或错误信息
    data: Order[];          // 订单数据数组
  }
  
  // 定义获取订单详情返回的结果结构
  export interface GetOrderDetailResponse {
    code: number;           // 状态码，0 表示成功，其他值表示失败
    msg: string;            // 状态信息或错误信息
    data: Order;            // 单个订单数据
  }
  
  // 定义创建订单返回的结果结构
  export interface CreateOrderResponse {
    code: number;           // 状态码，0 表示成功，其他值表示失败
    msg: string;            // 状态信息或错误信息
    data: Order;            // 新创建的订单数据
  }
  