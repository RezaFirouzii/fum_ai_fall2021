import java.awt.*;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class RBFS {

    private static class Entry {
        int f, g, h;
        State parent;
        State state;
        private Entry(int g, State parent, State state) {
            this.h = heuristic(parent, state);
            this.g = g;
            this.f = g + this.h;
            this.parent = parent;
            this.state = state;
        }
    }

    private static class Pair {
        boolean first;
        int second;
        private Pair(boolean first, int second) {
            this.first = first;
            this.second = second;
        }
    }

    public static void search(State initialState) {
        rbfs(new Entry(0, null, initialState), Integer.MAX_VALUE);
    }

    private static Pair rbfs(Entry current, int limit) {
        boolean ans = false;
        if (isGoal(current.state)) {
            result(current.state);
            return new Pair(true, -1);
        }
        var children = current.state.successor();
        if (children.isEmpty())
            return new Pair(false, Integer.MAX_VALUE);

        var queue = new ArrayList<Entry>();
        children.forEach(child -> queue.add(new Entry(current.g + 1, current.state, child)));
        while (!queue.isEmpty()) {
            queue.sort(Comparator.comparing(entry -> entry.f));
            var best = queue.get(0);
            if (best.f > limit)
                return new Pair(false, best.f);
            var alternative = queue.get(1);
            var res = rbfs(best, Math.min(alternative.f, limit));
            ans = res.first;
            best.f = res.second;
            queue.set(0, best);

            if (ans)
                break;
        }
        return new Pair(ans, -1);
    }

    private static int heuristic(State parent, State current) {
        int h = 0;
        if (parent == null)
            parent = current;
        for (int i = 0; i < parent.getGraph().size(); i++)
            if (parent.getGraph().getNode(i).getColor() != Color.Green &&
                    current.getGraph().getNode(i).getColor() != Color.Green)
                h += 1;

        return h;
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
            FileWriter myWriter = new FileWriter("RBFS_Result.txt");
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


