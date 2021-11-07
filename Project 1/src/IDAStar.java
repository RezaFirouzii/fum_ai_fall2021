import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class IDAStar {

    public static void search(State initialState) {
        var cutoff = heuristic(null, initialState);
        while (true) {
            System.out.printf("Iteration with cutoff: %d\n", cutoff);
            int distance = iterativeDeepeningAStar(null, initialState, 0, cutoff);
            if (distance == Integer.MAX_VALUE) {
                System.out.println("Search finished! NO final state found!");
                break;
            } else if (distance < 0) {
                System.out.printf("Cost: %d", -distance);
                break;
            } else cutoff = distance;
        }
    }

    private static int iterativeDeepeningAStar(State parent, State current, int distance, int cutoff) {

        if (isGoal(current)) {
            result(current);
            return -distance;
        }

        int f_score = distance + heuristic(parent, current);
        if (f_score > cutoff)
            return f_score;

        int min = Integer.MAX_VALUE;
        var children = current.successor();
        for (var child: children) {
            int d = iterativeDeepeningAStar(current, child, distance + 1, cutoff);
            if (d < 0)
                return d;
            else if (d < min)
                min = d;
        }
        return min;
    }


        private static int heuristic(State parent, State current) {
        int h = 0;
        if (parent == null)
            parent = current;
        for (int i = 0; i < parent.getGraph().size(); i++)
            if (parent.getGraph().getNode(i).getColor() != Color.Green &&
                    current.getGraph().getNode(i).getColor() != Color.Green)
                h++;

        return h / 2;
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
            FileWriter myWriter = new FileWriter("IDAstar_Result.txt");
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


