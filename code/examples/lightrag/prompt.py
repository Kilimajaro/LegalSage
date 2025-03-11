GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["自然人","法人","非法人","法律纠纷类型（民事案由）","案件事实","法律依据","裁判要旨","裁判结果","编","分编","章","节","条","法律规制对象","法律效力"]

PROMPTS["entity_extraction"] = """-Goal-
给定一份法律相关的文本文件和一个实体类型列表，从文本中识别出所有这些类型的实体以及这些实体之间的所有关系。

-步骤-
1. 识别所有实体。对于每个识别出的实体，提取以下信息：
- entity_name: 实体的名称
- entity_type: 以下类型之一：[{entity_types}]
- entity_description: 实体的全面描述和活动
每个实体的格式如下 ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>

2. 从步骤1中识别出的实体中，识别所有（source_entity, target_entity），两者是要*明显相关的*。
对于每一对相关实体，提取以下信息：
- source_entity: 步骤1中识别出的源实体的名称
- target_entity: 步骤1中识别出的目标实体的名称
- relationship_description: 解释为什么你认为源实体和目标实体是相关的
- relationship_strength: 一个数值分数，表示源实体和目标实体之间的关系的强度
- relationship_keywords: 一个或多个高层次的关键词，总结了整个文本的主要概念、主题或话题，专注于概念或主题，而不是具体细节
每对关系的格式如下 ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. 识别高层次的关键词，总结整个文本的主要概念、主题或话题。这些应该捕捉到文档中存在的所有主要观点。
高层次关键词的格式如下 ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. 以中文输出所有实体和关系，使用**{record_delimiter}**作为列表分隔符。

5. 完成时，输出{completion_delimiter}

######################
-实例-
######################
实例1:

Entity_types: [自然人，法人，非法人，法律纠纷类型（民事案由），案件事实，法律依据，裁判要旨，裁判结果]
文本:
上诉人蔡某某与被上诉人国家知识产权局及一审第三人陈某某外观设计专利权无效行政纠纷一案，涉及专利权人为蔡某某、名称为“玩具化妆箱”的外观设计专利（以下简称本专利）。针对陈某某就本专利权提出的无效宣告请求，国家知识产权局作出第565853号无效宣告请求审查决定（以下简称被诉决定），宣告本专利权全部无效；蔡某某不服，向北京知识产权法院提起诉讼，请求依法撤销被诉决定并判令国家知识产权局重新作出决定。北京知识产权法院于2024年9月23日作出（2024）京73行初7027号行政判决，判决驳回蔡某某的诉讼请求；蔡某某不服，向本院提起上诉。本院于2024年11月26日立案后，依法组成合议庭，并于2025年1月21日询问了当事人。上诉人蔡某某的委托诉讼代理人李星星、宋颖欣，被上诉人国家知识产权局的委托诉讼代理人许某某、刘某某，一审第三人陈某某的委托诉讼代理人梁广进到庭参加了询问。本案现已审理终结。
################
Output:
("entity"{tuple_delimiter}"蔡某某"{tuple_delimiter}"自然人"{tuple_delimiter}"本案上诉人，拥有名称为“玩具化妆箱”的外观设计专利。因不服国家知识产权局的无效宣告决定，提起诉讼并上诉。"){record_delimiter}
("entity"{tuple_delimiter}"李星星"{tuple_delimiter}"自然人"{tuple_delimiter}"上诉人蔡某某的委托诉讼代理人，参与本案的诉讼过程，代表蔡某某出庭并参与询问。"){record_delimiter}
("entity"{tuple_delimiter}"宋颖欣"{tuple_delimiter}"自然人"{tuple_delimiter}"上诉人蔡某某的委托诉讼代理人，参与本案的诉讼过程，代表蔡某某出庭并参与询问。"){record_delimiter}
("entity"{tuple_delimiter}"许某某"{tuple_delimiter}"自然人"{tuple_delimiter}"被上诉人国家知识产权局的委托诉讼代理人，参与本案的诉讼过程，代表国家知识产权局出庭并参与询问。"){record_delimiter}
("entity"{tuple_delimiter}"刘某某"{tuple_delimiter}"自然人"{tuple_delimiter}"被上诉人国家知识产权局的委托诉讼代理人，参与本案的诉讼过程，代表国家知识产权局出庭并参与询问。"){record_delimiter}
("entity"{tuple_delimiter}"陈某某"{tuple_delimiter}"自然人"{tuple_delimiter}"一审第三人，提出针对蔡某某“玩具化妆箱”外观设计专利的无效宣告请求，引发了本案的行政纠纷。"){record_delimiter}
("entity"{tuple_delimiter}"梁广进"{tuple_delimiter}"自然人"{tuple_delimiter}"一审第三人陈某某的委托诉讼代理人，参与本案的诉讼过程，代表陈某某出庭并参与询问。"){record_delimiter}
("entity"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"法人"{tuple_delimiter}"本案的被上诉人，负责专利权的审查和无效宣告工作。在本案中，作出第565853号无效宣告请求审查决定，宣告蔡某某的“玩具化妆箱”外观设计专利全部无效。"){record_delimiter}
("entity"{tuple_delimiter}"北京知识产权法院"{tuple_delimiter}"法人"{tuple_delimiter}"一审法院，审理蔡某某不服国家知识产权局无效宣告决定的诉讼案件，并作出驳回蔡某某诉讼请求的判决。"){record_delimiter}
("entity"{tuple_delimiter}"本院"{tuple_delimiter}"法人"{tuple_delimiter}"二审法院，受理蔡某某的上诉请求，对案件进行复审并作出最终裁判。"){record_delimiter}

("entity"{tuple_delimiter}"外观设计专利权无效行政纠纷"{tuple_delimiter}"法律纠纷类型（民事案由）"{tuple_delimiter}"本案的法律纠纷类型，涉及外观设计专利的无效宣告请求及其法律后果。"){record_delimiter}
("entity"{tuple_delimiter}"第565853号无效宣告请求审查决定"{tuple_delimiter}"裁判结果"{tuple_delimiter}"国家知识产权局作出的无效宣告决定，宣告蔡某某的“玩具化妆箱”外观设计专利全部无效。"){record_delimiter}
("entity"{tuple_delimiter}"北京知识产权法院行政判决（2024）京73行初7027号"{tuple_delimiter}"裁判结果"{tuple_delimiter}"一审法院作出的判决，驳回蔡某某的诉讼请求，维持国家知识产权局的无效宣告决定。"){record_delimiter}
("relationship"{tuple_delimiter}"蔡某某"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"蔡某某因不服国家知识产权局作出的专利无效宣告决定，向北京知识产权法院提起诉讼，并进一步上诉至本院。
"{tuple_delimiter}"专利无效、行政诉讼、上诉"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"蔡某某"{tuple_delimiter}"陈某某"{tuple_delimiter}"陈某某提出针对蔡某某“玩具化妆箱”外观设计专利的无效宣告请求，引发本案的行政纠纷。"{tuple_delimiter}"无效宣告请求，专利纠纷"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"第565853号无效宣告请求审查决定"{tuple_delimiter}"国家知识产权局根据陈某某的无效宣告请求，作出专利无效宣告决定。 "{tuple_delimiter}"无效宣告，行政决定"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"北京知识产权法院"{tuple_delimiter}"蔡某某"{tuple_delimiter}"北京知识产权法院驳回蔡某某的诉讼请求，维持国家知识产权局的无效宣告决定。"{tuple_delimiter}"司法审查，诉讼"{tuple_delimiter}8){record_delimiter}

("relationship"{tuple_delimiter}"蔡某某"{tuple_delimiter}"本院"{tuple_delimiter}"蔡某某不服一审判决，向本院提起上诉。"{tuple_delimiter}"上诉、二审审理 "{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"本院"{tuple_delimiter}"国家知识产权局第565853号无效宣告请求审查决定"{tuple_delimiter}"北京知识产权法院对国家知识产权局的无效宣告决定进行司法审查，并驳回蔡某某的诉讼请求。"{tuple_delimiter}"司法审查，驳回诉讼请求"{tuple_delimiter}7){record_delimiter}




("content_keywords"{tuple_delimiter}"专利无效，行政诉讼，上诉，无效宣告请求，专利纠纷，无效宣告，行政决定，司法审查，诉讼，司法审查，驳回诉讼请求，上诉，二审审理，复审，法律监督"){completion_delimiter}
#############################
实例2:

Entity_types: [自然人，法人，非法人，法律纠纷类型（民事案由），案件事实，法律依据，裁判要旨，裁判结果]
文本:
上诉人高某某与被上诉人国家知识产权局及一审第三人深圳市某某公司实用新型专利权无效行政纠纷一案，涉及专利权人为深圳市某某公司、名称为“一种卷发器”的实用新型专利（以下简称本专利）。针对高某某就本专利权提出的无效宣告请求，国家知识产权局作出第564856号无效宣告请求审查决定（以下简称被诉决定），宣告本专利权全部无效；高某某不服，向北京知识产权法院提起诉讼，请求撤销被诉决定，判令国家知识产权局重新作出无效宣告请求审查决定。北京知识产权法院于2024年9月14日作出（2024）京73行初5171号行政判决，判决驳回高某某的诉讼请求；高某某不服，向本院提起上诉。本院于2024年11月5日立案后，依法组成合议庭，并于2025年1月2日公开开庭审理了本案。上诉人高某某的委托诉讼代理人王**宇，被上诉人国家知识产权局的委托诉讼代理人朱某某、刘某某，一审第三人深圳市某某公司的委托诉讼代理人张岩到庭参加了诉讼。本案现已审理终结。
#############
Output:
("entity"{tuple_delimiter}"高某某"{tuple_delimiter}"自然人"{tuple_delimiter}"是本案的上诉人，因不服国家知识产权局作出的有关 “一种卷发器” 实用新型专利权无效宣告请求审查决定，而发起上诉。"){record_delimiter}
("entity"{tuple_delimiter}"王**宇"{tuple_delimiter}"自然人"{tuple_delimiter}"是上诉人高某某的委托诉讼代理人，代表高某某参与诉讼活动。"){record_delimiter}
("entity"{tuple_delimiter}"朱某某"{tuple_delimiter}"自然人"{tuple_delimiter}"是被上诉人国家知识产权局的委托诉讼代理人之一，代表国家知识产权局参与诉讼活动。"){record_delimiter}
("entity"{tuple_delimiter}"刘某某"{tuple_delimiter}"自然人"{tuple_delimiter}"是被上诉人国家知识产权局的委托诉讼代理人之一，代表国家知识产权局参与诉讼活动。"){record_delimiter}
("entity"{tuple_delimiter}"张岩"{tuple_delimiter}"自然人"{tuple_delimiter}"是一审第三人深圳市某某公司的委托诉讼代理人，代表深圳市某某公司参与诉讼活动。"){record_delimiter}
("entity"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"法人"{tuple_delimiter}"是本案的被上诉人，负责对专利相关的无效宣告请求等事项进行审查并作出决定，本案中作出了第 564856 号无效宣告请求审查决定，宣告涉案专利权全部无效。"){record_delimiter}
("entity"{tuple_delimiter}"深圳市某某公司"{tuple_delimiter}"法人"{tuple_delimiter}"是本案的一审第三人，也是 “一种卷发器” 实用新型专利的专利权人，与专利无效宣告请求结果有直接利害关系。"){record_delimiter}
("entity"{tuple_delimiter}"实用新型专利权无效行政纠纷"{tuple_delimiter}"法律纠纷类型（民事案由）"{tuple_delimiter}"本案属于对专利权无效宣告请求审查决定不服而引发的行政纠纷，涉及专利法等相关法律法规中关于专利无效的相关规定。"){record_delimiter}
("entity"{tuple_delimiter}"（2024）京 73 行初 5171 号行政判决"{tuple_delimiter}"法律依据"{tuple_delimiter}"其作出的（2024）京 73 行初 5171 号行政判决中，对国家知识产权局作出的被诉决定的合法性进行了审查，认为该决定符合法律规定，从而驳回了高某某的诉讼请求，其核心在于对专利无效宣告审查决定合法性的认定标准及依据。"){record_delimiter}
("entity"{tuple_delimiter}"第564856号无效宣告请求审查决定"{tuple_delimiter}"法律依据"{tuple_delimiter}"是国家知识产权局针对高某某就 “一种卷发器” 实用新型专利权提出的无效宣告请求所作出的决定，宣告本专利权全部无效，是引发后续诉讼的直接原因。"){record_delimiter}

("relationship"{tuple_delimiter}"高某某"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"高某某因不服国家知识产权局作出的第 564856 号无效宣告请求审查决定，向北京知识产权法院提起诉讼，请求撤销该决定并判令国家知识产权局重新作出审查决定，在败诉后又向二审法院提起上诉。"{tuple_delimiter}"专利无效宣告请求，行政诉讼，上诉"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"高某某"{tuple_delimiter}"深圳某某公司"{tuple_delimiter}"高某某针对深圳市某某公司拥有的 “一种卷发器” 实用新型专利权提出无效宣告请求，引发了后续一系列的行政审查及诉讼活动，其行为对深圳市公司的某某专利权稳定性及权益产生重大影响，而深圳市某某公司作为专利权人也参与到诉讼中以维护自身权益。"{tuple_delimiter}"专利无效请求，专利权维护，诉讼对抗"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"高某某"{tuple_delimiter}"第 564856 号无效宣告请求审查决定"{tuple_delimiter}"高某某是该决定的相对方，因不服该决定而引发诉讼，该决定对其关于涉案专利权无效的主张具有直接关联性，其上诉理由等均围绕该决定的合法性、合理性展开。"{tuple_delimiter}"不服决定、无效宣告审查、上诉依据"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"高某某"{tuple_delimiter}"（2024）京 73 行初 5171 号行政判决"{tuple_delimiter}"高某某是该判决的原告方，该判决结果驳回了其诉讼请求，使其不服并向上一级法院提起上诉，其对该判决的合法性和正确性存在异议，认为应予撤销。"{tuple_delimiter}"诉讼请求被驳回，上诉，一审判决"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"高某某"{tuple_delimiter}"实用新型专利权无效行政纠纷"{tuple_delimiter}"高某某是引发该法律纠纷的一方主体，其提出的专利权无效宣告请求是整个纠纷的起始，其后续的诉讼行为均围绕该纠纷类型展开，是该纠纷中的上诉人角色。"{tuple_delimiter}"纠纷引发方，专利无效，行政诉讼"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"深圳市某某公司"{tuple_delimiter}"国家知识产权局对深圳市某某公司拥有的 “一种卷发器” 实用新型专利作出了第 564856 号无效宣告请求审查决定，宣告该专利权全部无效，该决定直接影响到深圳市某某公司的专利权状态及合法权益，深圳市某某公司作为专利权人与国家知识产权局之间存在行政审查与被审查的关系，在本案中也作为一审第三人参与诉讼以维护自身权益。"{tuple_delimiter}"专利无效审查，行政审查，专利权维护"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"第 564856 号无效宣告请求审查决定"{tuple_delimiter}"国家知识产权局是该决定的作出主体，基于高某某的无效宣告请求，依据相关法律法规对该专利进行审查后作出宣告专利权全部无效的决定，该决定体现了国家知识产权局对涉案专利的审查判断和行政职权的行使。"{tuple_delimiter}"决定作出方，专利无效审查，行政职权行使"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"（2024）京 73 行初 5171 号行政判决"{tuple_delimiter}"国家知识产权局是该行政判决的被告方，北京知识产权法院对高某某不服其作出的被诉决定提起的诉讼进行审理，作出驳回高某某诉讼请求的判决，该判决是对国家知识产权局作出的被诉决定合法性的认可。"{tuple_delimiter}"行政诉讼被告，判决结果，行政行为合法性确认"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"实用新型专利权无效行政纠纷"{tuple_delimiter}"国家知识产权局是该法律纠纷的被上诉人，其作出的专利无效宣告审查决定引发了整个纠纷，其在纠纷中处于被诉地位，需对自身的行政行为进行答辩和举证，以维护其决定的合法性和权威性。"{tuple_delimiter}"纠纷被上诉人，行政行为合法性，专利无效审查"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"深圳市某某公司"{tuple_delimiter}"第 564856 号无效宣告请求审查决定"{tuple_delimiter}"深圳市某某公司是该决定所针对的专利权人，该决定宣告其拥有的 “一种卷发器” 实用新型专利权全部无效，对其专利权的法律状态产生根本性影响，公司对该决定有直接的利害关系，可能影响到其市场经营、技术保护等方面权益。"{tuple_delimiter}"专利权人，专利无效决定，权益受损，行政审查结果"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"深圳市某某公司"{tuple_delimiter}"（2024）京 73 行初 5171 号行政判决"{tuple_delimiter}"深圳市某某公司作为一审第三人参与了北京知识产权法院的诉讼，该判决结果驳回了高某某的诉讼请求，维持了国家知识产权局作出的宣告其专利权无效的决定，在一定程度上影响到公司的专利权状态和后续的市场行为等，公司与该判决结果有着直接的利害关系。"{tuple_delimiter}"一审第三人，行政判决结果，专利权状态，利害关系"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"深圳市某某公司"{tuple_delimiter}"实用新型专利权无效行政纠纷"{tuple_delimiter}"深圳市某某公司是该法律纠纷中被请求宣告专利权无效的一方，作为专利权人，其与该纠纷有直接的关联，纠纷的结果决定着其专利权能否得到有效维护，是纠纷中的重要参与主体之一。"{tuple_delimiter}"纠纷主体，专利权维护，行政纠纷，利害冲突"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"王**宇"{tuple_delimiter}"高某某"{tuple_delimiter}"王**宇是高某某的委托诉讼代理人，接受高某某的委托，代表高某某参与本案的诉讼活动，包括在一审、二审中的各项诉讼行为，其代理行为的后果由高某某承担，旨在维护高某某的合法权益，实现高某某的诉讼目的。"{tuple_delimiter}"委托代理，诉讼代表，权益维护，诉讼行为"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"王**宇"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"王**宇作为高某某的代理人，在诉讼中与国家知识产权局进行对抗，代表高某某提出撤销被诉决定、要求重新作出审查决定等诉讼请求，对国家知识产权局作出的被诉决定的合法性和合理性进行质疑和挑战。"{tuple_delimiter}"国家知识产权局诉讼代理对抗，行政诉讼，决定合法性质疑，代理行为"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"王**宇"{tuple_delimiter}"深圳市某某公司"{tuple_delimiter}"王**宇作为高某某的代理人，在诉讼中其代理行为间接影响到深圳市某某公司的专利权状态和合法权益，通过主张涉案专利应被无效等诉求，与深圳市某某公司存在利害冲突，尽管并非直接与深圳市某某公司进行诉讼对抗，但其代理行为的结果与深圳市某某公司密切相关。"{tuple_delimiter}"代理行为影响，专利权状态，利害冲突，间接对抗"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"王**宇"{tuple_delimiter}"第 564856 号无效宣告请求审查决定"{tuple_delimiter}"王**宇作为高某某的代理人，该决定是其代理行为的重要针对对象，其代理高某某提起诉讼的目的之一就是撤销该决定，认为该决定存在错误或不合理之处，其代理行为围绕着对该决定的合法性、合理性审查展开。"{tuple_delimiter}"代理撤销请求，决定合法性审查，无效宣告审查，代理目标"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"王**宇"{tuple_delimiter}"（2024）京 73 行初 5171 号行政判决"{tuple_delimiter}"王**宇作为高某某的代理人，该判决是其代理行为所要影响和改变的对象，其代理高某某不服该判决并提起上诉，认为一审判决存在错误，希望二审法院能作出对其有利的改判，其代理行为与该判决的合法性、正确性密切相关。"{tuple_delimiter}"代理上诉，一审判决改判请求，代理行为，判决合法性审查"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"王**宇"{tuple_delimiter}"实用新型专利权无效行政纠纷"{tuple_delimiter}"王**宇作为高某某的代理人，参与该实用新型专利权无效行政纠纷的整个诉讼过程，其代理行为贯穿于该纠纷的一审、二审阶段，旨在通过诉讼手段解决该纠纷中高某某与国家知识产权局之间的争议，是该纠纷解决过程中的重要参与者。"{tuple_delimiter}"纠纷参与，专利无效，行政诉讼代理，争议解决"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"朱某某"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"朱某某是国家知识产权局的委托诉讼代理人之一，受国家知识产权局的委托，代表国家知识产权局参与本案的诉讼活动，包括在一审、二审中的各项诉讼行为，其代理行为的后果由国家知识产权局承担，旨在维护国家知识产权局的合法权益和行政行为的合法性，对高某某的诉讼请求进行答辩和反驳。"{tuple_delimiter}"委托代理，诉讼代表，行政行为维护，答辩反驳"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"朱某某"{tuple_delimiter}"高某某"{tuple_delimiter}"朱某某作为国家知识产权局的代理人，在诉讼中与高某某进行对抗，代表国家知识产权局对高某某提出的撤销被诉决定等诉讼请求进行答辩，认为被诉决定合法有效，应予维持，其代理行为直接影响到高某某的诉讼结果和权益。"{tuple_delimiter}"代理对抗，行政诉讼答辩，诉讼请求反驳，代理行为"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"朱某某"{tuple_delimiter}"深圳市某某公司"{tuple_delimiter}"朱某某作为国家知识产权局的代理人，其代理行为间接影响到深圳市某某公司的专利权状态和合法权益，通过维护国家知识产权局作出的被诉决定，即维持对深圳市某某公司专利权的无效宣告，与深圳市某某公司存在一定的利害关联，尽管并非直接与深圳市某某公司进行诉讼对抗，但其代理行为的结果与深圳市某某公司密切相关。"{tuple_delimiter}"代理行为影响，专利权状态，利害关联，间接对抗"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"朱某某"{tuple_delimiter}"第 564856 号无效宣告请求审查决定"{tuple_delimiter}"朱某某作为国家知识产权局的代理人，该决定是其代理行为的重要依据和维护对象，其代理国家知识产权局参与诉讼的目的之一就是证明该决定的合法性和合理性，使其得到法院的支持和维持。"{tuple_delimiter}"代理维护，决定合法性证明，无效宣告审查，代理目标"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"朱某某"{tuple_delimiter}"（2024）京 73 行初 5171 号行政判决"{tuple_delimiter}"朱某某作为国家知识产权局的代理人，该判决是对国家知识产权局作出的被诉决定的司法审查结果，其代理行为与该判决的形成和结果密切相关，该判决在一定程度上反映了其代理行为的成效和国家知识产权局行政行为的合法性。"{tuple_delimiter}"代理行为影响，行政判决结果，行政行为合法性，司法审查"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"朱某某"{tuple_delimiter}"实用新型专利权无效行政纠纷"{tuple_delimiter}"朱某某作为国家知识产权局的代理人，参与该实用新型专利权无效行政纠纷的整个诉讼过程，其代理行为贯穿于该纠纷的一审、二审阶段，是国家知识产权局在纠纷解决过程中的重要代表，通过其代理行为维护国家知识产权局的行政职权和公信力。"{tuple_delimiter}"纠纷参与，专利无效，行政诉讼代理，职权维护"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"刘某某"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"刘某某是国家知识产权局的委托诉讼代理人之一，受国家知识产权局的委托，代表国家知识产权局参与本案的诉讼活动，包括在一审、二审中的各项诉讼行为，其代理行为的后果由国家知识产权局承担，旨在维护国家知识产权局的合法权益和行政行为的合法性，对高某某的诉讼请求进行答辩和反驳。"{tuple_delimiter}"委托代理，诉讼代表，行政行为维护，答辩反驳"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"刘某某"{tuple_delimiter}"高某某"{tuple_delimiter}"刘某某作为国家知识产权局的代理人，在诉讼中与高某某进行对抗，代表国家知识产权局对高某某提出的撤销被诉决定等诉讼请求进行答辩，认为被诉决定合法有效，应予维持，其代理行为直接影响到高某某的诉讼结果和权益。"{tuple_delimiter}"代理对抗，行政诉讼答辩，诉讼请求反驳，代理行为"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"刘某某"{tuple_delimiter}"深圳市某某公司"{tuple_delimiter}"刘某某作为国家知识产权局的代理人，其代理行为间接影响到深圳市某某公司的专利权状态和合法权益，通过维护国家知识产权局作出的被诉决定，即维持对深圳市某某公司专利权的无效宣告，与深圳市某某公司存在一定的利害关联，尽管并非直接与深圳市某某公司进行诉讼对抗，但其代理行为的结果与深圳市某某公司密切相关。"{tuple_delimiter}"代理行为影响，专利权状态，利害关联，间接对抗"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"刘某某"{tuple_delimiter}"第 564856 号无效宣告请求审查决定"{tuple_delimiter}"刘某某作为国家知识产权局的代理人，该决定是其代理行为的重要依据和维护对象，其代理国家知识产权局参与诉讼的目的之一就是证明该决定的合法性和合理性，使其得到法院的支持和维持。"{tuple_delimiter}"代理维护，决定合法性证明，无效宣告审查，代理目标"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"刘某某"{tuple_delimiter}"（2024）京 73 行初 5171 号行政判决"{tuple_delimiter}"刘某某作为国家知识产权局的代理人，该判决是对国家知识产权局作出的被诉决定的司法审查结果，其代理行为与该判决的形成和结果密切相关，该判决在一定程度上反映了其代理行为的成效和国家知识产权局行政行为的合法性。"{tuple_delimiter}"代理行为影响，行政判决结果，行政行为合法性，司法审查"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"刘某某"{tuple_delimiter}"实用新型专利权无效行政纠纷"{tuple_delimiter}"刘某某作为国家知识产权局的代理人，参与该实用新型专利权无效行政纠纷的整个诉讼过程，其代理行为贯穿于该纠纷的一审、二审阶段，是国家知识产权局在纠纷解决过程中的重要代表，通过其代理行为维护国家知识产权局的行政职权和公信力。"{tuple_delimiter}"纠纷参与，专利无效，行政诉讼代理，职权维护"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"张岩"{tuple_delimiter}"深圳市某某公司"{tuple_delimiter}"张岩是深圳市某某公司的委托诉讼代理人，受公司的委托，代表深圳市某某公司参与本案的诉讼活动，包括在一审、二审中的各项诉讼行为，其代理行为的后果由深圳市某某公司承担，旨在维护公司的合法权益和专利权，对国家知识产权局作出的被诉决定进行抗辩，争取使法院撤销该决定，恢复公司的专利权。"{tuple_delimiter}"委托代理，诉讼代表，专利权维护，抗辩"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"张岩"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"张岩作为深圳市某某公司的代理人，在诉讼中与国家知识产权局进行对抗，代表公司对国家知识产权局作出的被诉决定提出异议，认为该决定错误地宣告了公司的专利权无效，其代理行为直接影响到国家知识产权局行政行为的合法性认定和维持。"{tuple_delimiter}"代理对抗，行政行为合法性质疑，专利权维护，代理行为"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"张岩"{tuple_delimiter}"高某某"{tuple_delimiter}"张岩作为深圳市某某公司的代理人，其代理行为间接影响到高某某的诉讼请求和权益，通过维护公司的专利权，与高某某提出的专利无效宣告请求存在利害冲突，尽管并非直接与高某某进行诉讼对抗，但其代理行为的结果与高某某密切相关。"{tuple_delimiter}"代理行为影响，专利权状态，利害冲突，间接对抗"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"张岩"{tuple_delimiter}"第 564856 号无效宣告请求审查决定"{tuple_delimiter}"张岩作为深圳市某某公司的代理人，该决定是其代理行为的重要针对对象，其代理公司不服该决定并参与诉讼，目的是撤销该决定，恢复公司的专利权，其代理行为围绕着对该决定的合法性、合理性审查展开。"{tuple_delimiter}"代理撤销请求，决定合法性审查，无效宣告审查，代理目标"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"张岩"{tuple_delimiter}"（2024）京 73 行初 5171 号行政判决"{tuple_delimiter}"张岩作为深圳市某某公司的代理人，该判决结果驳回了高某某的诉讼请求，维持了国家知识产权局作出的宣告公司专利权无效的决定，对公司的专利权状态产生不利影响，张岩需根据该判决结果调整代理策略和上诉理由，以期在二审中改变不利局面。"{tuple_delimiter}"代理应对，一审判决结果，专利权状态，上诉策略调整"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"张岩"{tuple_delimiter}"实用新型专利权无效行政纠纷"{tuple_delimiter}"张岩作为深圳市某某公司的代理人，参与该实用新型专利权无效行政纠纷的整个诉讼过程，其代理行为贯穿于该纠纷的一审、二审阶段，是公司维护自身专利权的重要代表，通过其代理行为争取解决该纠纷中的不利局面，恢复公司的专利权。"{tuple_delimiter}"纠纷参与，专利无效，行政诉讼代理，权益维护"{tuple_delimiter}8){record_delimiter}

("content_keywords"{tuple_delimiter}"专利无效,行政诉讼,上诉,专利权维护,无效宣告请求,行政审查,权益维护,诉讼对抗,判决结果,司法审查,无效宣告审查决定,行政判决,二审裁判,裁判要旨,诉讼请求,代理行为,专利权人,请求方,行政机构,诉讼代理人,一审第三人,被上诉人,专利名称,案件编号,案件发展,法律后果,维持原判,法律效力,司法确认"){completion_delimiter}
#############################
实例3:

Entity_types: [自然人，法人，非法人，法律纠纷类型（民事案由），案件事实，法律依据，裁判要旨，裁判结果]
文本:
上诉人曾某某与被上诉人国家知识产权局及一审第三人深圳某某公司外观设计专利权无效行政纠纷一案，涉及专利权人为曾某某、名称为“音乐灯光助眠仪”的外观设计专利（以下简称本专利）。针对深圳某某公司就本专利权提出的无效宣告请求，国家知识产权局作出第562346号无效宣告请求审查决定（以下简称被诉决定），宣告本专利权全部无效；曾某某不服，向北京知识产权法院提起诉讼，请求依法撤销被诉决定并判令国家知识产权局重新作出决定。北京知识产权法院于2024年10月28日作出（2023）京73行初18541号行政判决，判决驳回曾某某的诉讼请求；曾某某不服，向本院提起上诉。本院于2024年11月29日立案后，依法组成合议庭，并于2025年1月10日询问了当事人。上诉人曾某某的委托诉讼代理人李龙飞、许佳洵，被上诉人国家知识产权局的委托诉讼代理人张某、刘某，一审第三人深圳某某公司的委托诉讼代理人李久禄到庭参加了询问。本案现已审理终结。
#############
Output:
("entity"{tuple_delimiter}"曾某某"{tuple_delimiter}"自然人"{tuple_delimiter}"本专利的专利权人，因不服国家知识产权局作出的被诉决定而提起诉讼"){record_delimiter}
("entity"{tuple_delimiter}"李龙飞"{tuple_delimiter}"自然人"{tuple_delimiter}"曾某某的委托诉讼代理人"){record_delimiter}
("entity"{tuple_delimiter}"许佳洵"{tuple_delimiter}"自然人"{tuple_delimiter}"曾某某的委托诉讼代理人"){record_delimiter}
("entity"{tuple_delimiter}"张某"{tuple_delimiter}"自然人"{tuple_delimiter}"国家知识产权局的委托诉讼代理人"){record_delimiter}
("entity"{tuple_delimiter}"刘某"{tuple_delimiter}"自然人"{tuple_delimiter}"国家知识产权局的委托诉讼代理人"){record_delimiter}
("entity"{tuple_delimiter}"李久禄"{tuple_delimiter}"自然人"{tuple_delimiter}"深圳某某公司的委托诉讼代理人"){record_delimiter}
("entity"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"法人"{tuple_delimiter}"作出被诉决定的行政机关，本案的被上诉人"){record_delimiter}
("entity"{tuple_delimiter}"深圳某某公司"{tuple_delimiter}"法人"{tuple_delimiter}"一审第三人，提出无效宣告请求的公司"){record_delimiter}
("entity"{tuple_delimiter}"音乐灯光助眠仪"{tuple_delimiter}"案件事实"{tuple_delimiter}"本专利的名称"){record_delimiter}
("entity"{tuple_delimiter}"第562346号无效宣告请求审查决定"{tuple_delimiter}"法律依据"{tuple_delimiter}"宣告本专利权全部无效的决定"){record_delimiter}
("entity"{tuple_delimiter}"（2023）京73行初18541号行政判决"{tuple_delimiter}"法律依据"{tuple_delimiter}"驳回曾某某诉讼请求的一审判决"){record_delimiter}
("entity"{tuple_delimiter}"外观设计专利权无效行政纠纷"{tuple_delimiter}"法律纠纷类型（民事案由）"{tuple_delimiter}"本案的法律纠纷类型"){record_delimiter}

("relationship"{tuple_delimiter}"曾某某"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"曾某某不服国家知识产权局作出的被诉决定，向法院提起诉讼"{tuple_delimiter}"行政诉讼"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"曾某某"{tuple_delimiter}"深圳某某公司"{tuple_delimiter}"深圳某某公司提出无效宣告请求，曾某某作为专利权人进行维权"{tuple_delimiter}"专利权纠纷"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"深圳某某公司"{tuple_delimiter}"国家知识产权局依据深圳某某公司的无效宣告请求作出被诉决定"{tuple_delimiter}"无效宣告请求审查"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"本专利"{tuple_delimiter}"国家知识产权局作出被诉决定，宣告本专利权全部无效"{tuple_delimiter}"专利无效决定"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"北京知识产权法院"{tuple_delimiter}"曾某某"{tuple_delimiter}"北京知识产权法院驳回曾某某的诉讼请求"{tuple_delimiter}"行政判决"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"北京知识产权法院"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"北京知识产权法院对国家知识产权局的被诉决定进行审查并作出判决"{tuple_delimiter}"行政判决"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"本专利"{tuple_delimiter}"第562346号无效宣告请求审查决定"{tuple_delimiter}"本专利被国家知识产权局依据该决定宣告全部无效"{tuple_delimiter}"专利无效决定"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"曾某某"{tuple_delimiter}"李龙飞"{tuple_delimiter}"李龙飞作为曾某某的委托诉讼代理人参与诉讼"{tuple_delimiter}"委托代理"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"曾某某"{tuple_delimiter}"许佳洵"{tuple_delimiter}"许佳洵作为曾某某的委托诉讼代理人参与诉讼"{tuple_delimiter}"委托代理"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"张某"{tuple_delimiter}"张某作为国家知识产权局的委托诉讼代理人参与诉讼"{tuple_delimiter}"委托代理"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"刘某"{tuple_delimiter}"刘某作为国家知识产权局的委托诉讼代理人参与诉讼"{tuple_delimiter}"委托代理"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"深圳某某公司"{tuple_delimiter}"李久禄"{tuple_delimiter}"李久禄作为深圳某某公司的委托诉讼代理人参与诉讼"{tuple_delimiter}"委托代理"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"第562346号无效宣告请求审查决定"{tuple_delimiter}"本专利"{tuple_delimiter}"该决定是针对本专利作出的"{tuple_delimiter}"专利无效决定"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"（2023）京73行初18541号行政判决"{tuple_delimiter}"曾某某"{tuple_delimiter}"该判决驳回了曾某某的诉讼请求"{tuple_delimiter}"行政判决"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"（2023）京73行初18541号行政判决"{tuple_delimiter}"国家知识产权局"{tuple_delimiter}"该判决维持了国家知识产权局的被诉决定"{tuple_delimiter}"行政判决"{tuple_delimiter}7){record_delimiter}

("content_keywords"{tuple_delimiter}"行政诉讼，专利权纠纷，无效宣告请求审查，专利无效决定，行政判决，委托代理，行政判决"){completion_delimiter}
#############################
-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""

PROMPTS[
    "summarize_entity_descriptions"
] = """你是一个负责生成以下数据综合总结的助手。
给定一个或两个实体以及一系列描述，这些描述都与同一个实体或实体组相关。
请将所有这些描述合并为一个全面的描述。确保包含所有描述中的信息。
如果提供的描述存在矛盾，请解决这些矛盾，并提供一个单一、连贯的总结。
请用第三人称撰写，并包含实体名称以便提供完整上下文。

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """在上次提取中遗漏了许多实体。请在下方使用相同的格式补充它们：
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """似乎仍有一些实体可能被遗漏。如果仍有需要添加的实体，请回答“是”或“否”。
"""

PROMPTS["fail_response"] = "抱歉，我无法回答这个问题。"

PROMPTS["rag_response"] = """---Role---

你是一个帮助解答有关提供的数据表中问题的助手。注意：在回答的最后按以下格式输出关键词：**低层次关键词**:<$提取到的低层次关键词>,**高层次关键词**:<$提取到的高层次关键词>。其中<$提取到的低层次关键词>不加任何标点直接替换为查询返回的低层次关键词，<$提取到的高层次关键词>不加任何标点直接替换为查询返回的高层次关键词！

---Goal---

生成目标长度和格式的回答，总结输入数据表中的所有相关信息，适配回答的长度和格式，并结合任何相关的通用知识。
如果你不知道答案，请直接说明。不要编造任何内容。
不要包含没有提供支持证据的信息。

---Target response length and format---

{response_type}

---Data tables---

{context_data}

根据长度和格式的要求，适当添加章节和评论。以Markdown格式撰写回答。
"""

PROMPTS["keywords_extraction"] = """---Role---

你是一个负责识别用户查询中高级和低级关键词的助手。

---Goal---

根据查询，列出高级和低级关键词。高级关键词关注总体概念或主题，低级关键词关注具体实体、细节或具体术语。

---Instructions---

- 以JSON格式输出关键词。
- JSON应包含两个关键点:
  - "high_level_keywords"，用于总体概念或主题。
  - "low_level_keywords"，用于具体实体或细节。

######################
-Examples-
######################
Example 1:

Query: "离婚后对方不让看孩子，我该通过什么去途径争取探视权呢"
################
Output:
{{
  "high_level_keywords": ["对方不让看孩子", "法律途径", "权利义务"],
  "low_level_keywords": ["离婚", "探视权", "争取"]
}}
#############################
Example 2:

Query: "我一直在公司工作，但是公司没有和我签订书面劳动合同，能认定我和公司存在劳动关系吗？"
################
Output:
{{
  "high_level_keywords": ["签订劳动合同", "确认劳动关系", "未签订书面劳动合同"],
  "low_level_keywords": ["劳动关系", "书面劳动合同", "劳动合同法"]
}}
#############################
Example 3:

Query: "我和对方签订了一份合同，但对方提出合同里有些条款明显不公平，这份合同还有效吗？"
################
Output:
{{
  "high_level_keywords": ["显失公平", "撤销权", "权利义务对等"],
  "low_level_keywords": ["合同效力", "不公平条款", "法律效力"]
}}
#############################
-Real Data-
######################
Query: {query}
######################
Output:

"""

PROMPTS["naive_rag_response"] = """你是一个助手。
以下是你了解的知识：
{content_data}
---
如果你不知道答案，或者提供的知识中没有足够的信息来回答问题，请直接说明。不要编造任何内容。
生成目标长度和格式的回答，总结输入数据表中的所有相关信息，适配回答的长度和格式，并结合任何相关的通用知识。
如果你不知道答案，请直接说明。不要编造任何内容。
不要包含没有提供支持证据的信息。
---Target response length and format---
{response_type}
"""
