import streamlit as st
import requests
import json
import public_ip as ipf

#get image from flask

def main():
    if "ip" not in st.session_state:
        st.session_state.ip = ipf.get() + ":443/back-end" # localhost:5000 for local use
    st.title("Cat or Dog classifier")

    uploaded_files = st.file_uploader("Choose an image here:", accept_multiple_files=False, type=['jpg','png','jpeg'])
    

    if uploaded_files is not None:
        if "upfile" not in st.session_state:
            st.session_state.upfile = uploaded_files
        elif uploaded_files != st.session_state.upfile:
            for key in st.session_state.keys():
                if key != "ip":
                    del st.session_state[key]
            st.session_state.upfile = uploaded_files
            

        img = uploaded_files.getvalue()


        if "id" not in st.session_state:
            id = requests.post(f"http://{st.session_state.ip}/save/", data = img)
            id = json.loads(id.text)
            st.session_state.id = id['id']
        
        if "id" in st.session_state:
            # load image from database
            link = requests.get(f"http://{st.session_state.ip}/data/{st.session_state.id}")
            st.markdown(f"""<img src="data:png;base64,{link.json()[0]}" width='700' height='700' >""", True)


            col1, col2 = st.columns([0.55,0.45])
            st.write("#")
            with col1:
                
                #uploaded_files = st.file_uploader("Choose an image here:", accept_multiple_files=False,type=['jpg','png','jpeg'])
                # send image to flask --> to database
                

                # get image classification
                st.write("##")
                st.write("##")
                if 'prediction' not in st.session_state:
                    if id['class'] == "0.0":
                        animal = 'cat'
                    else:
                        animal = 'dog'
                    st.session_state.prediction = animal


                st.subheader(f'Image classified as **{st.session_state.prediction}**')

            with col2:

                st.write("#")
                st.write('Is the classification correct?')
                st.write('Give us feedback for improvement')
                def saveright():
                    res = requests.post(f"http://{st.session_state.ip}/save/{st.session_state.id}", data = st.session_state.prediction)
                
                def savefalse():
                    if st.session_state.prediction == 'dog':
                        animal = 'cat'
                    else:
                        animal = 'dog'
                    res = requests.post(f"http://{st.session_state.ip}/save/{st.session_state.id}", data = animal)
                col2a, col2b, col2c,col2d = st.columns([0.05,0.3,0.3,0.35])
                with col2b:
                    st.button('right', on_click=saveright,type='secondary')
                with col2c:
                    st.button('wrong', on_click=savefalse,type='secondary')
    elif uploaded_files is None and "id" in st.session_state:
        for key in st.session_state.keys():
            if key != "ip":
                del st.session_state[key]




if __name__ == "__main__":
    main()


