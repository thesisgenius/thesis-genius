import Box1Display from "../components/BoxComponents/Box1Display";
import Box1Text from "../components/BoxComponents/Box1Text";
import Box2Display from "../components/BoxComponents/Box2Display";
import Box2Text from "../components/BoxComponents/Box2Text";
import Box3Display from "../components/BoxComponents/Box3Display";
import Box3Text from "../components/BoxComponents/Box3Text";
import Box4Display from "../components/BoxComponents/Box4Display";
import Box4Text from "../components/BoxComponents/Box4Text";
import Box5Display from "../components/BoxComponents/Box5Display";
import Box5Text from "../components/BoxComponents/Box5Text";
import Box6Display from "../components/BoxComponents/Box6Display";
import Box6Text from "../components/BoxComponents/Box6Text";
import MainDisplay from "../components/BoxComponents/MainDisplay";
import MainText from "../components/BoxComponents/MainText";
import "../styles/ThesisPages.css";

//This page incorporates all of the textarea and display components
//It also 
const AllPages = () => {
    return (

            //
        <main class="container">
            <section class="card left-card">
            <h1>Thesis Input</h1>
            

                <Box1Text />
                <Box2Text />
                <Box3Text />
                <Box4Text />
                <Box5Text />
                <Box6Text />

                <MainText />
                <MainText />
                <MainText />


            </section>


            <section class="card right-card">
            <h1>Thesis Output</h1>

                <Box1Display />
                <Box2Display />
                <Box3Display />
                <Box4Display />
                <Box5Display />
                <Box6Display />

                <MainDisplay />
                <MainDisplay />
                <MainDisplay />


            </section>
        </main>

    );
};

export default AllPages;
