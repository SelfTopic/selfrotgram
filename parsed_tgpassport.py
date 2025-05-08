
# class: start
class PassportData(BaseModel):
    data: Union[List[EncryptedPassportElement]]
    credentials: EncryptedCredentials
# class: end

# class: start
class PassportFile(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int
# class: end

# class: start
class EncryptedPassportElement(BaseModel):
    type: str
    data: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    files: Optional[Union[List[PassportFile]]] = None
    front_side: Optional[Union[PassportFile]] = None
    reverse_side: Optional[Union[PassportFile]] = None
    selfie: Optional[Union[PassportFile]] = None
    translation: Optional[Union[List[PassportFile]]] = None
    hash: str
# class: end

# class: start
class EncryptedCredentials(BaseModel):
    data: str
    hash: str
    secret: str
# class: end

# class: start
@dataclass
class SetPassportDataErrors(TelegramAPIMethod):
    __api_method__: ClassVar[str] = "setPassportDataErrors"
    user_id: int
    errors: Union[List[PassportElementError]]
# class: end

# class: start
PassportElementError = Union[PassportElementErrorDataField, PassportElementErrorFrontSide, PassportElementErrorReverseSide, PassportElementErrorSelfie, PassportElementErrorFile, PassportElementErrorFiles, PassportElementErrorTranslationFile, PassportElementErrorTranslationFiles, PassportElementErrorUnspecified]
# class: end

# class: start
class PassportElementErrorDataField(BaseModel):
    source: str
    type: str
    field_name: str
    data_hash: str
    message: str
# class: end

# class: start
class PassportElementErrorFrontSide(BaseModel):
    source: str
    type: str
    file_hash: str
    message: str
# class: end

# class: start
class PassportElementErrorReverseSide(BaseModel):
    source: str
    type: str
    file_hash: str
    message: str
# class: end

# class: start
class PassportElementErrorSelfie(BaseModel):
    source: str
    type: str
    file_hash: str
    message: str
# class: end

# class: start
class PassportElementErrorFile(BaseModel):
    source: str
    type: str
    file_hash: str
    message: str
# class: end

# class: start
class PassportElementErrorFiles(BaseModel):
    source: str
    type: str
    file_hashes: List[str]
    message: str
# class: end

# class: start
class PassportElementErrorTranslationFile(BaseModel):
    source: str
    type: str
    file_hash: str
    message: str
# class: end

# class: start
class PassportElementErrorTranslationFiles(BaseModel):
    source: str
    type: str
    file_hashes: List[str]
    message: str
# class: end

# class: start
class PassportElementErrorUnspecified(BaseModel):
    source: str
    type: str
    element_hash: str
    message: str
# class: end
