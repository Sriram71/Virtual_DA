import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import speech_recognition as sr
import io
import pyttsx3

# Load the CSV file into a DataFrame
data = r"C:\Users\Sriram\Downloads\car_Dekho_DA.csv"
df = pd.read_csv(data)

# Store all fuel types in a list
fuel_types = df['Fuel_Type'].unique().tolist()

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    print(text)  # Print the text
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio"
        except sr.RequestError:
            print("Could not request results; check your network connection")
            return ""

def num_vehicles():
    num_cars = len(df)
    return f"There are {num_cars} vehicles"

def Year_Models():
    max_year = df["Year"].max()
    min_year = df["Year"].min()
    return f"Our vehicles range from {min_year} to {max_year}"

def Lowest_price():
    min_price = df["Selling_Price"].min()
    return f"It is {min_price} lakh"

def low_price_Vehicle():
    min_price_vehicle = df.loc[df["Selling_Price"] == df["Selling_Price"].min(), "Car_Name"].values[0]
    return min_price_vehicle

def heighest_price():
    max_price = df["Selling_Price"].max()
    return f"It is {max_price} lakhs"


def high_price_Vehicle():
    max_price_vehicle = df.loc[df["Selling_Price"] == df["Selling_Price"].max(), "Car_Name"].values[0]
    return max_price_vehicle

def Info_data():
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    print(info_str)  # Print the full DataFrame info
    columns = ", ".join(df.columns)
    return f"{columns}."

def pie_chart(column_name):
    if column_name not in df.columns:
        return f"Sorry, the column '{column_name}' is not present in the DataFrame."
    try:
        plt.pie(df[column_name].value_counts(), labels=df[column_name].unique(), shadow=True)
        plt.title(f"Distribution of {column_name}")
        plt.show()
    except Exception as e:
        return "Sorry, it can't be given in a pie chart"

def no_of_vehicles_fuel(fuel):
    no_of_veh = (df["Fuel_Type"] == fuel).sum()  # Correctly count the number of vehicles with the specified fuel type
    return f"There are {no_of_veh} vehicles of {fuel} type"

def all_vehicles_fuel(fuel):
    vehicles_with_fuel = df[df["Fuel_Type"] == fuel]
    return vehicles_with_fuel

df['depreciation'] = df['Present_Price'] - df['Selling_Price']

def max_depreciation():
    return df.loc[df.depreciation == df.depreciation.max()]

def min_depreciation():
    return df.loc[df.depreciation == df.depreciation.min()]

def count_values_in_column(column_name):
    if column_name not in df.columns:
        return f"Sorry, the column '{column_name}' is not present in the DataFrame."
    count = df[column_name].count()
    return count



def plot_bargraph(column_name):
    if column_name not in df.columns:
        return f"Sorry, the column '{column_name}' is not present in the DataFrame."
    df[column_name].value_counts().plot.bar()
    plt.xlabel(column_name)
    plt.ylabel("Count")
    plt.title(f"Bar Graph of {column_name}")
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels if needed
    plt.tight_layout()  # Adjust layout for better spacing
    plt.show()

def sns_countplot(column_name):
    if column_name not in df.columns:
        return f"Sorry, the column '{column_name}' is not present in the DataFrame."
    try:
        fig_dims = (12, 10)  # Adjust figure size as needed
        fig, ax = plt.subplots(figsize=fig_dims)
        sns.countplot(y=df[column_name], ax=ax, data=df)
        plt.title(f"Countplot of {column_name}")
        plt.xlabel("Count")
        plt.ylabel(column_name)
        plt.show()
    except Exception as e:
        return "Sorry, it can't be given in a bar graph"

def Owned_veh():
    return df.Owner.value_counts()

def count_unique_vehicles():
    unique_vehicles = df['Car_Name'].nunique()
    return f"There are {unique_vehicles} unique vehicles in the dataset."

def plot_scatter(x_column, y_column):
    if x_column not in df.columns or y_column not in df.columns:
        return f"Sorry, either '{x_column}' or '{y_column}' is not present in the DataFrame."
    plt.scatter(df[x_column], df[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{y_column} vs {x_column}")
    plt.show()

two_wheelers = df[df["Present_Price"] < 3.5]
two_wheelers = two_wheelers.loc[two_wheelers.Car_Name != "alto k10"]
two_wheelers = two_wheelers.loc[two_wheelers.Car_Name != "omni"]
two_wheelers = two_wheelers.loc[two_wheelers.Car_Name != "800"]

def Ind_vehicle():
    m = df["Seller_Type"].value_counts()
    ind_count = m["Individual"]
    return (f"There are {ind_count} vehicles slled by individuals")

def Deal_vehicle():
    m = df["Seller_Type"].value_counts()
    ind_count = m["Dealer"]
    return (f"There are {ind_count} vehicles selled by Dealers")

def extract_fuel_type_from_command(command):
    for fuel in fuel_types:
        if fuel.lower() in command:
            return fuel
    return None

def extract_column_name_from_command(command):
    command = command.replace(" ", "_")
    for col in df.columns:
        if col.lower() in command:
            return col
    return None

def extract_two_column_names_from_command(command):
    command = command.replace(" ", "_")
    command = command.lower()
    columns = df.columns.str.lower()
    found_columns = []

    for col in columns:
        if col in command:
            found_columns.append(col)
            if len(found_columns) == 2:
                break

    if len(found_columns) == 2:
        return df.columns[columns == found_columns[0]].values[0], df.columns[columns == found_columns[1]].values[0]
    else:
        return None, None


def main():
    speak("Hello, how can I help you today?")
    while True:
        command = listen().lower()
        if "hello" in command:
            speak("Hi there! How can I assist you?")
        elif "your name" in command or "are you" in command:
            speak("I am a Virtual Data Analyst created by Sriram.")
        elif "my name is" in command:
            name = extract_name_from_command(command)
            enter_name(name)
            speak(f"Nice to meet you, {name}!")
        elif ("what" in command or "details" in command) and"data" in command:
            speak(Info_data())
        elif "year" in command and "vehicle" in command:
            speak(Year_Models())
        elif "highest price" in command and "vehicle" in command:
            speak(high_price_Vehicle())
            speak(heighest_price())
        elif "low price" in command or "least price" in command and "vehicle" in command:
            speak(low_price_Vehicle())
            speak(Lowest_price())
        elif "scatter plot" in command or "scatter" in command:
            x_column, y_column = extract_two_column_names_from_command(command)
            if x_column and y_column:
                speak(f"Creating a scatter plot of {y_column} vs {x_column}")
                plot_scatter(x_column, y_column)
            else:
                speak("Sorry, I couldn't identify two valid columns for the scatter plot.")
        elif "pie chart" in command or "visualisation" in command and "circle graph" in command:
            col_name = extract_column_name_from_command(command)
            if col_name:
                speak(f"Drawing pie chart for {col_name}")
                pie_chart(col_name)
            else:
                speak("Sorry, I couldn't identify the column you specified in the dataset")
        elif "count plot" in command or "seaborn" in command and "graph" in command:
            col_name = extract_column_name_from_command(command)
            if col_name:
                speak(f" Here is the graph for {col_name}")
                sns_countplot(col_name)
            else:
                speak("Sorry, I couldn't identify the column you specified in the dataset")
        elif "bar graph" in command or "plot" in command and "graph" in command and "count plot"not in command and "seaborn"not in command:
            col_name = extract_column_name_from_command(command)
            if col_name:
                speak(f" Here is the bar graph for {col_name}")
                plot_bargraph(col_name)
            else:
                speak("Sorry, I couldn't identify the column you specified in the dataset")
        elif ("how many " in command or "how much" in command) and "column" in command:
            col_name = extract_column_name_from_command(command)
            if col_name:
                tot=count_values_in_column(col_name)
                speak(f"total values in  {col_name} are {tot}")
            else:
                speak("Sorry, I couldn't identify the column you specified in the dataset")
        elif "how many" in command and ("petrol" in command or "cng" in command or "diesel" in command) and "vehicle" in command:
            fuel_type = extract_fuel_type_from_command(command)
            if fuel_type:
                speak(no_of_vehicles_fuel(fuel_type))
            else:
                speak("Sorry, I couldn't identify the fuel type.")
        elif "all" in command and ("petrol" in command or "cng" in command or "diesel" in command) and "vehicle" in command:
                fuel_type = extract_fuel_type_from_command(command)
                if fuel_type:
                    speak("HERE ARE THE LIST OF VEHICLES YOU ASKED FOR")
                    print(all_vehicles_fuel(fuel_type))
                else:
                    speak("Sorry, I couldn't identify the fuel type in the data set.")
        elif "minimum" in command or"least" in command and "depreciation" in command :
            speak('The minimum depreciation vehicle')
            speak(min_depreciation())
        elif "individual" in command  and"vehicle" in command :
            speak(Ind_vehicle())
        elif "dealer" in command and"vehicle" in command :
            speak(Deal_vehicle())
        elif "depreciation" in command and "maximum" in command or "highest" in command:
            speak('The maximum depreciation vehicle')
            speak(max_depreciation())
        elif "depreciation" in command and "what is" in command and "min" not in command and "max" not in command :
            speak('Depreciation refers to the reduction in the value of an asset over time')
            speak('That is present price is subracted with selling price')
        elif "price" in command or "what is" in command and"heigh" in command and "costly" in command or "expensive" in command :
            speak('The most expencive car is ')
            speak(high_price_Vehicle())
        elif "price" in command or "what is" in command and "least" in command or"cheap" in command or "economy" in command and "depreciation" not in command:
            speak('the least cost vehicle is  ')
            speak(low_price_Vehicle())
        elif "owned " in command or "owned vehicle" in command:
            speak(Owned_veh())
        elif "unique" in command and 'vehicle' in command:
            speak(count_unique_vehicles())
        elif "many" in command and "vehicle" in command and "fuel" not in command and "petrol" not in command and "cng" not in command and "diesel" not in command and "unique" not in command and "own" not in command:
            speak(num_vehicles())
        elif "exit" in command or "bye" in command or "tata" in command or 'quit'in command or "see you later" in command or "shut up" in command:
            speak("Thank you for your time. It was a pleasure talking with you")
            break
        else:
            speak("I am sorry, I do not understand that command.")

def extract_name_from_command(command):
    return command.split("my name is", 1)[1].strip()

def enter_name(name):
    global user_name
    user_name = name

if __name__ == "__main__":
    main()