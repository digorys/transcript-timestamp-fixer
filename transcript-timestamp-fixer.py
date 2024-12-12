import re
import streamlit as st

def adjust_transcript(transcript: str) -> str:
    # Find all timestamps
    timestamps = re.findall(r'(\d{2}:\d{2}:\d{2}\.\d{3})', transcript)

    assert len(timestamps) % 2 == 0, \
        'Number of timestamps should be even'

    assert timestamps[2::2] == sorted(timestamps[2::2]), \
        'Timestamps should be in ascending order'

    # Create a list of adjusted end timestamps
    adjusted_timestamps = timestamps[2:-1:2] + ['00:00:00.000']

    assert len(adjusted_timestamps) == len(timestamps) // 2, \
        'Number of adjusted timestamps should be half the number of timestamps'
    
    # Adjust the timestamps in the transcript
    adjusted_transcript = re.sub(
        r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})',
        lambda m: f"{m.group(1)} --> {adjusted_timestamps.pop(0)}",
        transcript
    )

    new_timestamps = re.findall(r'(\d{2}:\d{2}:\d{2}\.\d{3})', adjusted_transcript)

    assert len(timestamps) == len(new_timestamps), \
        'Number of timestamps should remain the same'

    assert timestamps[0::2] == new_timestamps[0::2], \
        'Start timestamps should remain the same'

    assert timestamps[2::2] == new_timestamps[1:-1:2], \
        'End timestamps should match the start timestamps'

    assert new_timestamps[-1] == '00:00:00.000', \
        'Last timestamp should be 00:00:00.000'

    assert timestamps[0:-2:2] < new_timestamps[1:-1:2], \
        'Adjusted end timestamps should be greater than start timestamps'
    
    assert len(transcript) == len(adjusted_transcript), \
        'Length of the transcript should remain the same'
    
    return adjusted_transcript

################################# Streamlit UI #################################

st.set_page_config(layout="wide")

st.title("Transcript Timestamp Fixer \U0001FA84")

st.write("Paste your transcript below:")
transcript = st.text_area("Input Transcript", height=300)

# Adjust and preview button
if st.button("Fix Transcript"):
    try:
        # Process the transcript
        adjusted_transcript = adjust_transcript(transcript)
        
        # Display the adjusted transcript
        st.subheader("Fixed Transcript:")
        st.text_area("Output transcript", adjusted_transcript, height=300)
        
    except Exception as e:
        st.error(f"Error: {e}")
