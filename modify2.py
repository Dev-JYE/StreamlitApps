import streamlit as st

def remove_text(target_text, text_to_remove):
    lines = target_text.split('\n')
    new_lines = []

    for line in lines:
        new_line = line.replace(text_to_remove, "")
        new_lines.append(new_line)

    new_text = '\n'.join(new_lines)
    return new_text

def main():
    st.title("Text Editor")

    target_text = st.text_area("텍스트를 입력하세요:", "")
    text_to_remove = st.text_input("제거할 텍스트를 입력하세요:", "")

    if st.button("제거"):
        if target_text and text_to_remove:
            new_text = remove_text(target_text, text_to_remove)
            st.subheader("수정된 텍스트:")
            st.text_area("결과:", value=new_text)  # 결과가 입력창에 나타남

            # 클립보드로 'new_text' 복사
            st.experimental_set_query_params(new_text=new_text)  # new_text를 쿼리 매개변수로 설정
            st.experimental_rerun()  # 쿼리 매개변수를 사용하여 앱 재실행

            st.success("수정된 텍스트가 클립보드에 복사되었습니다!")
        else:
            st.warning("대상 텍스트와 제거할 텍스트를 모두 입력하세요.")

    # 'new_text' 쿼리 매개변수를 가져와서 클립보드로 복사
    new_text_query_param = st.experimental_get_query_params().get("new_text", None)
    if new_text_query_param:
        st.experimental_rerun()  # 변경사항을 표시하지 않고 앱을 재실행

if __name__ == "__main__":
    main()
