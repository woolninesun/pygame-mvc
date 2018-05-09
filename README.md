# PygameMVC
the framework base on [pygame](https://www.pygame.org) library

---
由於 pygame 只能跑在 main thread，很難用 multi thread 去跑。有兩種策略
1. 通通跑在 main thread
2. view 和 control 跑在 main thread (因為需要用到 pygame)，然後 model 跑在 other thread

但由於 python 受到 GIL 限制，multi thread 效用不大，所以採用第一種策略去寫
