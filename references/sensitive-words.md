# 敏感词与高风险词汇库

## 使用说明

本库按风险类型分类，用于 listing 内容的自动敏感词匹配。
扫描时，出现以下词汇不自动等于违规，需结合上下文和使用方式综合判断。

---

## 第一类：平台禁用词（各大平台 listing 明确禁止）

### 促销/价格类
```
英文：
sale, on sale, clearance, discount, % off, percent off
bogo, buy one get one, buy 2 get 1, bundle deal
flash sale, lightning deal, limited time offer, today only
last chance, hurry, act now, order now（促销语气）
free shipping（listing 正文，非配送选项）
free gift, free item, bonus item（listing 标题）
lowest price, best price, cheapest, price match

中文：
促销、打折、优惠、买一送一、限时、秒杀、抢购
最低价、跳楼价、出血价、亏本价
```

### 联系方式类（全平台禁用）
```
英文：
www., .com, .net, .org, .cn, http, https
@（邮箱格式）, email us, contact us, call us
whatsapp, wechat, line, telegram, kakao
follow us, subscribe, instagram, facebook, tiktok, youtube
phone, tel, fax, hotline

中文：
微信、公众号、抖音号、关注我们、扫码、二维码
电话、客服、联系方式
```

### 评价操控类（全平台禁用）
```
英文：
leave a review, leave feedback, rate us
5-star, five star review, positive feedback
delete review, remove feedback, change rating
in exchange for, in return for（+review）
rebate, refund（+review）

中文：
好评返现、留评返现、五星好评、给个好评
删除差评、修改评价
```

---

## 第二类：广告法违禁词

### 中国广告法绝对禁用词（极限词）
```
最高级词：
最好、最棒、最优、最强、最大、最小、最快、最慢
最高、最低、最多、最少、最实惠、最超值
最权威、最专业、最安全、最有效、最放心

唯一性词：
唯一、第一、首个、首家、独家、独有、专属
国内首家、全国唯一、行业首创

顶级词：
顶级、顶尖、极致、终极、极品、至尊、无上
臻品、臻享（用于最高级声称时）

国际/国家背书（无授权）：
国家级、国际级、世界级、全球领先
国家推荐、政府认可、央视认证、国家标准
```

### 英文广告禁用词模式
```
绝对化：
best, finest, greatest, ultimate, unsurpassed, unmatched
world's best, #1, number one, top-rated（无依据）
perfect, flawless, ideal, superior（绝对用法）

虚假保证：
guaranteed, 100% guaranteed, money-back guaranteed（无条件）
no risk, risk-free, nothing to lose
always works, never fails, zero complaints

无依据专业背书：
doctor-recommended（无真实推荐）
clinically proven（无临床研究）
scientifically proven（无科学依据）
fda approved（未经 FDA 批准）
award-winning（无真实奖项）
```

---

## 第三类：医疗/健康违规词汇

### 疾病声称（非药品/医疗器械不得使用）
```
英文疾病词：
cure, treat, heal, remedy（+疾病名）
prevent, fight, combat（+疾病名）
therapy, therapeutic, medicinal, pharmaceutical
diagnose, clinical, prescription

常见违规搭配：
- helps treat / cures / eliminates + [任何疾病名称]
疾病名称举例：cancer, diabetes, arthritis, depression,
anxiety, insomnia, hypertension, alzheimer's,
adhd, autism, eczema, psoriasis...

中文疾病词：
治疗、治愈、根治、消除、控制（+疾病）
预防疾病、防癌、抗癌、降血糖、降血压
改善×× 症、缓解×× 症状（+疾病名）
```

### 身体声称（敏感）
```
英文：
weight loss（声称+具体数字）
fat burning, metabolism boost（强声称）
muscle gain（无运动前提的声称）
detox, detoxify, cleanse（内脏解毒）
anti-aging（声称逆龄，非外观改善）

中文：
减肥、瘦身（+确定性承诺）
排毒、清毒
增高（成人产品）
丰胸、增大（成人保健品）
壮阳、补肾（保健品监管词汇）
```

---

## 第四类：知识产权高风险词汇

### 高风险品牌词（直接使用须警惕）

**科技品牌：**
```
Apple, iPhone, iPad, MacBook, iMac, AirPods, Apple Watch, iOS
Samsung, Galaxy, Note, Bixby
Google, Pixel, Android, Nest, Chromecast
Microsoft, Xbox, Surface, Windows
Sony, PlayStation, Walkman, Bravia
Amazon, Kindle, Alexa, Fire TV
Meta, Facebook, Instagram, WhatsApp, Oculus
```

**服装/运动品牌：**
```
Nike, Swoosh, Jordan, Air Force, Air Max
Adidas, Yeezy, Stan Smith, Superstar
Puma, Reebok, New Balance, Asics, Hoka
Lululemon, Patagonia, North Face, Columbia
Gucci, LV, Louis Vuitton, Chanel, Hermes, Prada
Rolex, Omega, Cartier（手表）
```

**娱乐/IP 品牌：**
```
Disney, Marvel, DC Comics, Star Wars, Pixar
Mickey Mouse, Spider-Man, Batman, Wonder Woman
LEGO, Barbie, Hot Wheels, Nerf
Pokémon, Pikachu, Hello Kitty, Sanrio, Doraemon
Nintendo, Mario, Zelda, Splatoon
Harry Potter, Hogwarts
```

### 侵权暗示词汇
```
英文：
[brand]-style, [brand]-inspired, [brand]-like
similar to [brand], looks like [brand]
genuine, authentic, original, official（+他人品牌）
replica, copy, clone（明示仿冒）

中文：
[品牌]同款、[品牌]风格、[品牌]平替
仿[品牌]、类[品牌]
与[品牌]相同、媲美[品牌]
```

---

## 第五类：政治/地缘敏感词

### 全球通用敏感话题
```
争议领土：台湾独立、西藏独立、香港独立
政治人物批评（尤其中东王室、中国领导人）
宗教冒犯（各主要宗教）
种族歧视词汇
```

### 中国市场特别敏感
```
政治：民主、自由（政治语境）、天安门事件
领土：台湾、西藏、香港（与主权相关表述）
历史：文化大革命（负面表述）
领导人：习近平、毛泽东（调侃/批评）
```

### 中东市场特别敏感
```
宗教：对伊斯兰的不尊重表述
地缘：以色列/巴勒斯坦政治立场
社会：LGBTQ 相关内容（多国禁止）
```

---

## 第六类：安全/危险品相关

### 危险暗示词（需核实合规性）
```
英文：
explosives, explosive, detonator（爆炸物）
military grade, tactical, weapon（军事用途）
surveillance（隐藏式监控）
untraceable, ghost（枪支改造语境）
```

### 进出口管制暗示词
```
dual-use（军民两用）
EAR, ITAR（出口管制）
encrypted（加密设备）
night vision（夜视设备，部分国家出口管制）
```

---

## 第七类：语气/表述风险词

### 过度承诺类（🟡 MEDIUM）
```
英文：
lifetime guarantee, lifetime warranty（需真实支撑）
unbreakable, indestructible（绝对物理声称）
waterproof（需标注 IP 等级，否则可能误导）
permanent, forever, never（效果声称）

中文：
终身保修、永久有效、永不生锈
100%防水（未标等级）
绝对安全、零风险
```

### 虚假紧迫/稀缺词（🟡 MEDIUM）
```
英文：
only X left in stock（虚假库存数量）
selling fast（无真实数据）
price going up soon（无真实依据）
limited edition（实际非限量）

中文：
仅剩×件（虚假）、即将断货（虚假）
限量版（实际非限量）
价格即将上涨（无依据）
```

---

## 扫描优先级建议

1. **先扫第四类（IP 品牌词）**：最常见的严重违规来源
2. **次扫第一类（平台禁用）**：直接触发下架
3. **次扫第三类（医疗词汇）**：高法律风险
4. **再扫第二类（广告法极限词）**：中国市场重点
5. **最后扫其余类**：补充低风险提示
