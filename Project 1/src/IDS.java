import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class IDS {

    public static boolean search(State initialState, int maxDepth) {
        for (int i = 0; i < maxDepth; i++) {
            if (DLS(initialState, i))
                return true;
        }
        return false;
    }

    private static boolean DLS(State currentState, int depth) {
        if (isGoal(currentState)) {
            result(currentState);
            return true;
        }
        if (depth <= 0) return false;

        ArrayList<State> children = currentState.successor();
        for (var child: children)
            if (DLS(child, depth - 1))
                return true;
        return false;
    }

    private static boolean isGoal(State state){
        for (int i = 0; i < state.getGraph().size(); i++) {
            if(state.getGraph().getNode(i).getColor() == Color.Red
                    || state.getGraph().getNode(i).getColor() == Color.Black){
                return false;
            }
        }
        return true;
    }

    private static void result(State state){
        Stack<State>  states = new Stack<State>();
        while (true){
            states.push(state);
            if(state.getParentState() == null){
                break;
            }
            else {
                state = state.getParentState();
            }
        }
        try {
            FileWriter myWriter = new FileWriter("IDS_Result.txt");
            System.out.println("initial state : ");
            while (!states.empty()){
                State tempState = states.pop();
                if(tempState.getSelectedNodeId() != -1) {
                    System.out.println("selected id : " + tempState.getSelectedNodeId());
                }
                tempState.getGraph().print();

                myWriter.write(tempState.getSelectedNodeId()+" ,");
                myWriter.write(tempState.outputGenerator()+"\n");
            }
            myWriter.close();
            System.out.println("Successfully wrote to the file.");
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }
}


