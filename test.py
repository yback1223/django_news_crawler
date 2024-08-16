import re
import json

# test.txt 파일에서 텍스트 읽기
with open('test.txt', 'r', encoding='utf-8') as file:
    raw_text = file.read()


# 텍스트에서 ```json``` 부분 제거
cleaned_text = re.sub(r'^```json|```$', '', raw_text.strip(), flags=re.MULTILINE)
if cleaned_text[-2] != '"':
    cleaned_text = cleaned_text[:-1] + '"' + cleaned_text[-1:]


# 결과 출력
print("Cleaned text:")
print(cleaned_text)

# 파싱 가능한 경우, 딕셔너리로 변환
try:
    result_dict = json.loads(cleaned_text, strict=False)
    print("\nParsed dictionary:")
    print(result_dict)
    print(f"result_dict['translated_headline'] = {result_dict['translated_headline']}")
    print(f"result_dict['summarized_content'] = {result_dict['summarized_content']}")

except json.JSONDecodeError as e:
    print(f'\nFailed to parse JSON: {e}')
