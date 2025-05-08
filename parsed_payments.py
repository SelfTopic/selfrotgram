
# class: start
@dataclass
class SendInvoice(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "sendInvoice"
    chat_id: Union[int, str]
    message_thread_id: Optional[int] = None
    title: str
    description: str
    payload: str
    provider_token: Optional[str] = None
    currency: str
    prices: List[LabeledPrice]
    max_tip_amount: Optional[int] = None
    suggested_tip_amounts: Optional[List[int]] = None
    start_parameter: Optional[str] = None
    provider_data: Optional[str] = None
    photo_url: Optional[str] = None
    photo_size: Optional[int] = None
    photo_width: Optional[int] = None
    photo_height: Optional[int] = None
    need_name: Optional[bool] = None
    need_phone_number: Optional[bool] = None
    need_email: Optional[bool] = None
    need_shipping_address: Optional[bool] = None
    send_phone_number_to_provider: Optional[bool] = None
    send_email_to_provider: Optional[bool] = None
    is_flexible: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[ReplyParameters] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
# class: end

# class: start
@dataclass
class CreateInvoiceLink(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "createInvoiceLink"
    business_connection_id: Optional[str] = None
    title: str
    description: str
    payload: str
    provider_token: Optional[str] = None
    currency: str
    prices: List[LabeledPrice]
    subscription_period: Optional[int] = None
    max_tip_amount: Optional[int] = None
    suggested_tip_amounts: Optional[List[int]] = None
    provider_data: Optional[str] = None
    photo_url: Optional[str] = None
    photo_size: Optional[int] = None
    photo_width: Optional[int] = None
    photo_height: Optional[int] = None
    need_name: Optional[bool] = None
    need_phone_number: Optional[bool] = None
    need_email: Optional[bool] = None
    need_shipping_address: Optional[bool] = None
    send_phone_number_to_provider: Optional[bool] = None
    send_email_to_provider: Optional[bool] = None
    is_flexible: Optional[bool] = None
# class: end

# class: start
@dataclass
class AnswerShippingQuery(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "answerShippingQuery"
    shipping_query_id: str
    ok: bool
    shipping_options: Optional[List[ShippingOption]] = None
    error_message: Optional[str] = None
# class: end

# class: start
@dataclass
class AnswerPreCheckoutQuery(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "answerPreCheckoutQuery"
    pre_checkout_query_id: str
    ok: bool
    error_message: Optional[str] = None
# class: end

# class: start
@dataclass
class GetStarTransactions(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "getStarTransactions"
    offset: Optional[int] = None
    limit: Optional[int] = None
# class: end

# class: start
@dataclass
class RefundStarPayment(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "refundStarPayment"
    user_id: int
    telegram_payment_charge_id: str
# class: end

# class: start
@dataclass
class EditUserStarSubscription(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "editUserStarSubscription"
    user_id: int
    telegram_payment_charge_id: str
    is_canceled: bool
# class: end

# class: start
class LabeledPrice(BaseModel):
    label: str
    amount: int
# class: end

# class: start
class Invoice(BaseModel):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int
# class: end

# class: start
class ShippingAddress(BaseModel):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str
# class: end

# class: start
class OrderInfo(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    shipping_address: Optional[ShippingAddress] = None
# class: end

# class: start
class ShippingOption(BaseModel):
    id: str
    title: str
    prices: List[LabeledPrice]
# class: end

# class: start
class SuccessfulPayment(BaseModel):
    currency: str
    total_amount: int
    invoice_payload: str
    subscription_expiration_date: Optional[int] = None
    is_recurring: Optional[bool] = None
    is_first_recurring: Optional[bool] = None
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
# class: end

# class: start
class RefundedPayment(BaseModel):
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: Optional[str] = None
# class: end

# class: start
class ShippingQuery(BaseModel):
    id: str
    user: User = Field(alias="from")
    invoice_payload: str
    shipping_address: ShippingAddress
# class: end

# class: start
class PreCheckoutQuery(BaseModel):
    id: str
    user: User = Field(alias="from")
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None
# class: end

# class: start
class PaidMediaPurchased(BaseModel):
    user: User = Field(alias="from")
    paid_media_payload: str
# class: end

# class: start
RevenueWithdrawalState = Union[RevenueWithdrawalStatePending, RevenueWithdrawalStateSucceeded, RevenueWithdrawalStateFailed]
# class: end

# class: start
class RevenueWithdrawalStatePending(BaseModel):
    type: str
# class: end

# class: start
class RevenueWithdrawalStateSucceeded(BaseModel):
    type: str
    date: int
    url: str
# class: end

# class: start
class RevenueWithdrawalStateFailed(BaseModel):
    type: str
# class: end

# class: start
class AffiliateInfo(BaseModel):
    affiliate_user: Optional[User] = None
    affiliate_chat: Optional[Chat] = None
    commission_per_mille: int
    amount: int
    nanostar_amount: Optional[int] = None
# class: end

# class: start
TransactionPartner = Union[TransactionPartnerUser, TransactionPartnerChat, TransactionPartnerAffiliateProgram, TransactionPartnerFragment, TransactionPartnerTelegramAds, TransactionPartnerTelegramApi, TransactionPartnerOther]
# class: end

# class: start
class TransactionPartnerUser(BaseModel):
    type: str
    transaction_type: str
    user: User
    affiliate: Optional[AffiliateInfo] = None
    invoice_payload: Optional[str] = None
    subscription_period: Optional[int] = None
    paid_media: Optional[List[PaidMedia]] = None
    paid_media_payload: Optional[str] = None
    gift: Optional[Gift] = None
    premium_subscription_duration: Optional[int] = None
# class: end

# class: start
class TransactionPartnerChat(BaseModel):
    type: str
    chat: Chat
    gift: Optional[Gift] = None
# class: end

# class: start
class TransactionPartnerAffiliateProgram(BaseModel):
    type: str
    sponsor_user: Optional[User] = None
    commission_per_mille: int
# class: end

# class: start
class TransactionPartnerFragment(BaseModel):
    type: str
    withdrawal_state: Optional[RevenueWithdrawalState] = None
# class: end

# class: start
class TransactionPartnerTelegramAds(BaseModel):
    type: str
# class: end

# class: start
class TransactionPartnerTelegramApi(BaseModel):
    type: str
    request_count: int
# class: end

# class: start
class TransactionPartnerOther(BaseModel):
    type: str
# class: end

# class: start
class StarTransaction(BaseModel):
    id: str
    amount: int
    nanostar_amount: Optional[int] = None
    date: int
    source: Optional[TransactionPartner] = None
    receiver: Optional[TransactionPartner] = None
# class: end

# class: start
class StarTransactions(BaseModel):
    transactions: List[StarTransaction]
# class: end
