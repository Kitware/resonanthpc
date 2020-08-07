<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <!-- TODO: this is very basic implementation of nka_bt_ats - by no means complete -->
    <AttDef Type="time integrator" BaseType="" Version="0">
      <ItemDefinitions>

        <!-- TOP level arguments -->
        <Void Name="extrapolate initial guess" Optional="true" IsEnabledByDefault="true"/>
        <Double Name="initial time step">
          <DefaultValue>86400.0</DefaultValue>
        </Double>
        <!-- SOLVER TYPE: `nka_bt_ats` -->

        <!-- nka_bt_ats parameters list section -->
        <Group Name="nka_bt_ats parameters">
          <ItemDefinitions>
            <Double Name="nonlinear tolerance">
              <DefaultValue>1.0e-6</DefaultValue>
            </Double>
            <Int Name="limit iterations">
              <DefaultValue>20</DefaultValue>
            </Int>
            <Double Name="diverged tolerance">
              <DefaultValue>1.0e10</DefaultValue>
            </Double>
            <Int Name="nka lag iterations">
              <DefaultValue>0</DefaultValue>
            </Int>
            <Int Name="max nka vectors">
              <DefaultValue>10</DefaultValue>
            </Int>
            <Double Name="nka vector tolerance">
              <DefaultValue>0.05</DefaultValue>
            </Double>
            <Double Name="backtrack tolerance">
              <DefaultValue>0.0</DefaultValue>
            </Double>
            <Double Name="backtrack factor">
              <DefaultValue>0.5</DefaultValue>
            </Double>
            <String Name="backtrack monitor">
              <DiscreteInfo DefaultIndex="0">
                <Value>monitor either</Value>
                <Value>monitor enorm</Value>
                <Value>monitor L2 residual</Value>
                <!-- should these two be different? docs say one, examples use other -->
                <Value>monitor residual</Value>
              </DiscreteInfo>
            </String>
            <Int Name="backtrack max steps">
              <!-- TODO: check name -->
              <DefaultValue>10</DefaultValue>
            </Int>
            <Int Name="backtrack max total steps">
              <DefaultValue>1e6</DefaultValue>
            </Int>
            <Int Name="backtrack lag iterations">
              <DefaultValue>0</DefaultValue>
            </Int>
            <Int Name="backtrack last iterations">
              <DefaultValue>1e6</DefaultValue>
            </Int>
            <Void Name="backtrack fail on bad search direction" Optional="true" IsEnabledByDefault="false"/>
            <!-- There can also be a verbosity here?? -->
            <!-- TODO: `Anderson mixing` and `relaxation parameter`-->

            <!-- max error growth factor: 1000.0-->
            <!-- modify correction: true -->

          </ItemDefinitions>
        </Group>

        <!-- verbose object -->
        <String Name="verbosity level">
          <DiscreteInfo DefaultIndex="0">
            <Value>low</Value>
            <Value>medium</Value>
            <Value>high</Value>
            <Value>extreme</Value>
          </DiscreteInfo>
        </String>

        <!-- timestep controller list section -->
        <!-- timestep controller type: smarter -->
        <Group Name="timestep controller smarter parameters">
          <ItemDefinitions>
            <Int Name="max iterations">
              <DefaultValue>18</DefaultValue>
            </Int>
            <Int Name="min iterations">
              <DefaultValue>10</DefaultValue>
            </Int>
            <Double Name="time step reduction factor">
              <DefaultValue>0.5</DefaultValue>
            </Double>
            <Double Name="time step increase factor">
              <DefaultValue>1.25</DefaultValue>
            </Double>
            <Double Name="max time step">
              <!-- <DefaultValue>63115.20</DefaultValue> -->
            </Double>
            <Double Name="min time step">
              <DefaultValue>1e-10</DefaultValue>
            </Double>
            <Int Name="growth wait after fail">
              <DefaultValue>2</DefaultValue>
            </Int>
            <Int Name="count before increasing increase factor">
              <DefaultValue>2</DefaultValue>
            </Int>
          </ItemDefinitions>
        </Group>

      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeResource>
