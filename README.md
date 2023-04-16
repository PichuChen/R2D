# R2D

Form Ragic! to Decanter, make your data ready for analysis.

## What is R2D?

R2D is a tool that helps you to send your data from Ragic! to Decanter.
Decanter is a data analysis tool that helps you to analyze your data.
And Ragic! is a cloud-based database that helps you to manage your data.

So you can got you data predict result from Decanter.

## How to use R2D?

1. Create a new Ragic! database.
2. Create a new Decanter project.
3. Create a new Ragic! sheet.
4. Get your Ragic! API key. (https://www.ragic.com/intl/zh-TW/doc-api/24/HTTP-Basic-authentication-with-Ragic-API-Key)
5. Get your Ragic parameters:
    * eg. https://ap9.ragic.com/decanter_titanic/train/1
    * RAGIC_HOST: ap9.ragic.com
    * RAGIC_AP_ID: decanter_titanic
    * RAGIC_TABLE_ID: train
    * RAGIC_SHEET_ID: 1
6. Get your Decanter API key.
7. Get your Decanter parameter's
    eg. ```
    curl -X POST "https://decanter.ai/v1/prediction/single_predict" -H "accept: application/json" \
        -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VE1NDc2NjguNTE0NjkxfQ.ze4hNEsYZWVbkQPC6I" \
        -H "Content-Type: application/json" \
        -d '{"project_id":"643a61bd29fb742b5641ad00","model_id":"643a6306fae26392c35ff190","experiment_id":"643a62e74a95a22bd9d48691","features":[{"PassengerId":1,"Survived":0,"Pclass":3,"Name":"Braund, Mr. Owen Harris","Sex":"male","Age":22,"SibSp":1,"Parch":0,"Ticket":"A/5 21171","Fare":7.25,"Cabin":"C85","Embarked":"S"}]}'
    ```
    * DECANTER_API_KEY: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VE1NDc2NjguNTE0NjkxfQ.ze4hNEsYZWVbkQPC6I
    * DECANTER_PROJECT_ID: 643a61bd29fb742b5641ad00
    * DECANTER_MODEL_ID: 643a6306fae26392c35ff190
    * DECANTER_EXPERIMENT_ID: 643a62e74a95a22bd9d48691 (optional)
8. Get ragic field ID.
9. Copy start.sh to start-user.sh
10. Fill your parameters in start-user.sh
11. Run start-user.sh


