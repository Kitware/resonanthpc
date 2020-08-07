<!-- These preconditioners are used by PKs. Once a user makes one, they must be selected from within a PK or they will not be used -->
<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <!-- Base class for all preconditioners -->
    <AttDef Type="preconditioner-base" BaseType="" Abstract="true" Version="0">
      <!-- preconditioner type -->
      <!-- _preconditioner_type_ parameters -->
    </AttDef>

    <AttDef Type="identity" Label="Identity" BaseType="preconditioner-base" Version="0">
      <!-- no parameters -->
    </AttDef>

    <AttDef Type="diagonal" Label="Diagonal" BaseType="preconditioner-base" Version="0">
      <!-- no parameters -->
    </AttDef>

    <AttDef Type="block ilu" Label="Block ILU" BaseType="preconditioner-base" Version="0">
      <ItemDefinitions>
        <Double Name="fact: relax value">
          <DefaultValue>1.0</DefaultValue>
        </Double>
        <Double Name="fact: absolute threshold">
          <DefaultValue>1.0</DefaultValue>
        </Double>
        <Double Name="fact: relative threshold">
          <DefaultValue>1.0</DefaultValue>
        </Double>
        <Int Name="fact: level-of-fill">
          <DefaultValue>0</DefaultValue>
        </Int>
        <Int Name="overlap">
          <DefaultValue>0</DefaultValue>
        </Int>
        <String Name="schwarz: combine mode">
          <DefaultValue>Add</DefaultValue>
        </String>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="boomer amg" Label="Boomer AMG" BaseType="preconditioner-base" Version="0">
      <!-- See https://github.com/amanzi/amanzi/blob/master/src/solvers/PreconditionerBoomerAMG.hh -->
      <ItemDefinitions>
        <Double Name="tolerance">
          <DefaultValue>0.0</DefaultValue>
        </Double>
        <Int Name="smoother sweeps">
          <DefaultValue>3</DefaultValue>
        </Int>
        <Int Name="cycle applications">
          <DefaultValue>5</DefaultValue>
        </Int>
        <Double Name="strong threshold">
          <DefaultValue>0.5</DefaultValue>
        </Double>
        <Int Name="relaxation type">
          <DefaultValue>6</DefaultValue>
        </Int>
        <Int Name="coarsen type">
          <DefaultValue>0</DefaultValue>
        </Int>
        <Int Name="max multigrid levels" Optional="true"></Int>
        <Void Name="use block indices" Optional="true" IsEnabledByDefault="false"></Void>
        <Int Name="number of functions">
          <DefaultValue>1</DefaultValue>
        </Int>
        <Int Name="nodal strength of connection norm">
          <DefaultValue>0</DefaultValue>
        </Int>
        <String Name="verbosity">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="summary of run time settings and timing information">0</Value>
            <Value Enum="coarsening info">1</Value>
            <Value Enum="smoothing info">2</Value>
            <Value Enum="both coarsening and smoothing">3</Value>
          </DiscreteInfo>
        </String>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="euclid" Label="Euclid" BaseType="preconditioner-base" Version="0">
      <ItemDefinitions>
        <Int Name="ilu(k) fill level">
          <DefaultValue>1</DefaultValue>
        </Int>
        <Double Name="ilut drop tolerance">
          <DefaultValue>0.0</DefaultValue>
        </Double>
        <Void Name="rescale row" Optional="true" IsEnabledByDefault="false"></Void>
        <String Name="verbosity">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="summary of run time settings and timing information">0</Value>
            <!-- TODO: docs don't list any other options? is this same as Boomer AMG? -->
          </DiscreteInfo>
        </String>

      </ItemDefinitions>
    </AttDef>

    <!-- TODO: ml preconditioner parameters are not listed... skipping -->
    <!-- <AttDef Type="preconditioner-ml" Label="TODO: ML (Trilinos AMG)" BaseType="preconditioner-base" Version="0"></AttDef> -->

  </Definitions>
</SMTK_AttributeResource>
